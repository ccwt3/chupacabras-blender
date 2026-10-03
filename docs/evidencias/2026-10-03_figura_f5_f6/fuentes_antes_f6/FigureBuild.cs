using System;
using System.IO;
using System.Linq;
using Chupacabras;
using UnityEditor;
using UnityEditor.Build;
using UnityEditor.Build.Reporting;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.Rendering.Universal;

public static class FigureBuild {
  public static bool Surface => Environment.GetEnvironmentVariable("CHUPA_FIGURE_STAGE") == "F4";
  public static string Stage => Surface ? "F4" : "F1";
  public static string Scene => "Assets/Scenes/" + Stage + "_FiguraAR_" + (Surface ? "r02" : "r01") + ".unity";
  public static string Folder => "Assets/FiguraAR/" + Stage + "_" + (Surface ? "r02" : "r01");
  public static string Version => Surface ? "0.2.0" : "0.1.0";
  public static string Evidence => Environment.GetEnvironmentVariable("CHUPA_FIGURE_EVIDENCE") ?? "docs/evidencias/F1_r01";
  public static void Configure() {
    TrackingBuild.RequireVersion();
    if (Surface) { FigureSurface.Configure(); return; }
    ExchangeBuild.Require(!File.Exists(Scene) && !Directory.Exists(Folder), "Preserve figure delivery");
    Directory.CreateDirectory(Folder);
    AssetDatabase.Refresh();
    // Copy only the figure and its lights, never the study component or its references.
    EditorSceneManager.OpenScene("Assets/Scenes/12_AppearanceAR_demacrado_r02.unity");
    var study = UnityEngine.Object.FindFirstObjectByType<AppearanceStudy>();
    var root = new GameObject("FigurePresentation");
    var figure = UnityEngine.Object.Instantiate(study.visualRoot.Find("StaticFigure").gameObject, root.transform);
    figure.name = "StaticFigure";
    foreach (var renderer in figure.GetComponentsInChildren<Renderer>()) {
      renderer.sharedMaterials = renderer.sharedMaterials.Select(material => {
        string target = Folder + "/" + material.name + ".mat";
        if (!File.Exists(target)) ExchangeBuild.Require(AssetDatabase.CopyAsset(AssetDatabase.GetAssetPath(material), target), "Copy material");
        return AssetDatabase.LoadAssetAtPath<Material>(target);
      }).ToArray();
    }
    UnityEngine.Object.Instantiate(study.visualRoot.Find("FigureFill").gameObject, root.transform).name = "FigureFill";
    var key = UnityEngine.Object.Instantiate(study.transform.Find("MoonKey").gameObject, root.transform);
    key.name = "FigureKey";
    key.GetComponent<Light>().cullingMask = 1;
    var pipeline = UnityEngine.Object.Instantiate(study.pipeline);
    pipeline.name = "FigureURP";
    AssetDatabase.CreateAsset(pipeline, Folder + "/FigureURP.asset");
    PrefabUtility.SaveAsPrefabAsset(root, Folder + "/Figure.prefab");
    var scene = EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Single);
    root = (GameObject)PrefabUtility.InstantiatePrefab(AssetDatabase.LoadAssetAtPath<GameObject>(Folder + "/Figure.prefab"));
    root.SetActive(false);
    var probe = new GameObject("FigureTracking").AddComponent<TrackingProbe>();
    probe.staticFigure = root.transform;
    probe.figurePipeline = pipeline;
    probe.unlitShader = Shader.Find("Universal Render Pipeline/Unlit");
    probe.litShader = Shader.Find("Universal Render Pipeline/Lit");
    RenderSettings.ambientMode = AmbientMode.Flat;
    RenderSettings.ambientLight = new Color(.23f, .27f, .36f);
    RenderSettings.skybox = null;
    RenderSettings.fog = false;
    AssetDatabase.SaveAssets();
    EditorSceneManager.SaveScene(scene, Scene);
  }
  public static void CheckDependencies(string[] dependencies) {
    var forbidden = dependencies.Where(p => p.StartsWith("Assets/") &&
      (p.Contains("/Appearance") || p.Contains("/Rigs/") || p.Contains("/Environment/") ||
       p.Contains("/Sheep/") || p.Contains("/Acting/") || p.Contains("/Blocking/") ||
       p.Contains("/Exchange/") || p.EndsWith(".renderTexture") || p.EndsWith(".playable"))).ToArray();
    // Runtime script references can retain class metadata, not historical scene assets.
    forbidden = forbidden.Where(p => !p.EndsWith(".cs")).ToArray();
    ExchangeBuild.Require(forbidden.Length == 0, "Cinematic dependencies: " + string.Join(", ", forbidden));
  }
  public static void Verify() {
    TrackingBuild.RequireVersion();
    Directory.CreateDirectory(Evidence);
    TrackingChecks.Run();
    EditorSceneManager.OpenScene(Scene);
    var probe = UnityEngine.Object.FindFirstObjectByType<TrackingProbe>();
    var root = probe.staticFigure;
    ExchangeBuild.Require(probe.appearance == null && root != null && !root.gameObject.activeSelf, "Figure starts hidden");
    ExchangeBuild.Require(root.Find("StaticFigure").localPosition == Vector3.zero, "Centered figure");
    ExchangeBuild.Require(root.GetComponentsInChildren<Animator>(true).Length == 0 &&
      root.GetComponentsInChildren<Camera>(true).Length == 0, "Static figure only");
    int triangles = root.GetComponentsInChildren<MeshFilter>(true).Sum(m => m.sharedMesh.triangles.Length / 3);
    ExchangeBuild.Require(triangles == (Surface ? FigureSurface.Triangles : 30880), "Preserve source mesh");
    string[] dependencies = AssetDatabase.GetDependencies(Scene, true);
    File.WriteAllLines(Evidence + "/scene_dependencies.txt", dependencies.OrderBy(p => p));
    CheckDependencies(dependencies);
    var previous = QualitySettings.renderPipeline;
    try {
      QualitySettings.renderPipeline = probe.figurePipeline;
      root.gameObject.SetActive(true);
      var view = new GameObject("VerificationCamera").AddComponent<Camera>();
      view.cullingMask = 1; view.clearFlags = CameraClearFlags.SolidColor;
      view.backgroundColor = new Color(.25f, .25f, .25f);
      view.nearClipPlane = .01f; view.farClipPlane = 10;
      view.fieldOfView = 38; view.aspect = 16f / 9;
      view.GetUniversalAdditionalCameraData();
      var marker = GameObject.CreatePrimitive(PrimitiveType.Quad);
      marker.name = "Marker_ONLY_FOR_VERIFICATION";
      marker.transform.position = new Vector3(0, 0, .001f);
      // Fixture detection square is 160/512; 320 mm yields 100 mm detection.
      marker.transform.localScale = new Vector3(.32f, .32f, 1);
      var material = new Material(probe.unlitShader);
      material.SetTexture("_BaseMap", Resources.Load<Texture2D>("AprilTagFixture"));
      marker.GetComponent<Renderer>().sharedMaterial = material;
      foreach (var angle in new[] { ("front", new Vector3(.015f, -.48f, -.30f)),
          ("left", new Vector3(-.35f, -.36f, -.30f)), ("right", new Vector3(.35f, -.36f, -.30f)) }) {
        view.transform.position = angle.Item2;
        view.transform.LookAt(new Vector3(0, 0, -.05f), Vector3.back);
        if (Surface) FigureSurface.Save(view, Evidence + "/composition_" + angle.Item1 + ".png", 960, 540);
        else ExchangeBuild.SaveCamera(view, Evidence + "/composition_" + angle.Item1 + ".png");
      }
      if (Surface) FigureSurface.VerifyViews(probe, view);
      File.WriteAllText(Evidence + "/checks.json", "{\"passed\":true,\"physicalDevice\":false,\"triangles\":" + triangles + ",\"views\":3,\"cinematicAssetDependencies\":0}\n");
    } finally { QualitySettings.renderPipeline = previous; }
  }
  public static void BuildAndroid() {
    TrackingBuild.RequireVersion();
    string product = PlayerSettings.productName, version = PlayerSettings.bundleVersion;
    int code = PlayerSettings.Android.bundleVersionCode;
    string id = PlayerSettings.GetApplicationIdentifier(NamedBuildTarget.Android);
    var pipeline = GraphicsSettings.defaultRenderPipeline;
    var quality = QualitySettings.renderPipeline;
    try {
      PlayerSettings.productName = "Chupacabras — Figura AR";
      PlayerSettings.bundleVersion = Version; PlayerSettings.Android.bundleVersionCode = Surface ? 200 : 100;
      PlayerSettings.SetApplicationIdentifier(NamedBuildTarget.Android, "com.chupacabras.ar.figure");
      GraphicsSettings.defaultRenderPipeline = AssetDatabase.LoadAssetAtPath<UniversalRenderPipelineAsset>(Folder + "/FigureURP.asset");
      QualitySettings.renderPipeline = GraphicsSettings.defaultRenderPipeline;
      string output = "builds/android/" + Stage + "_figure_" + DateTime.UtcNow.ToString("yyyyMMdd_HHmmss") + ".apk";
      ExchangeBuild.Require(!File.Exists(output), "Preserve APK");
      var report = BuildPipeline.BuildPlayer(new BuildPlayerOptions {
        scenes = new[] { Scene }, locationPathName = output, target = BuildTarget.Android,
        options = BuildOptions.Development | BuildOptions.DetailedBuildReport
      });
      File.WriteAllText(output + ".build.txt", $"Unity: {Application.unityVersion}\nResult: {report.summary.result}\nErrors: {report.summary.totalErrors}\nWarnings: {report.summary.totalWarnings}\nBytes: {report.summary.totalSize}\nDuration: {report.summary.totalTime}\nPhysical G20: pending\n");
      ExchangeBuild.Require(report.summary.result == BuildResult.Succeeded, "Figure APK failed");
      var assets = report.packedAssets.SelectMany(p => p.contents).Select(c => c.sourceAssetPath).Distinct().OrderBy(p => p).ToArray();
      File.WriteAllLines(Evidence + "/packed_assets.txt", assets);
      ExchangeBuild.Require(assets.Any(p => p.Contains(Surface ? "F3_chupacabras_superficie" : "09_chupacabras_demacrado")), "Build report contains figure mesh");
      CheckDependencies(assets);
      File.WriteAllText(Evidence + "/apk_path.txt", output + "\n");
      Debug.Log("CHUPACABRAS_FIGURE_APK " + output);
    } finally {
      PlayerSettings.productName = product; PlayerSettings.bundleVersion = version;
      PlayerSettings.Android.bundleVersionCode = code;
      PlayerSettings.SetApplicationIdentifier(NamedBuildTarget.Android, id);
      GraphicsSettings.defaultRenderPipeline = pipeline; QualitySettings.renderPipeline = quality;
      AssetDatabase.SaveAssets();
    }
  }
}
