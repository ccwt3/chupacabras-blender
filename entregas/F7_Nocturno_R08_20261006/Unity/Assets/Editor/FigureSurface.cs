using System;
using System.IO;
using System.Linq;
using Chupacabras;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.Rendering.Universal;

// F4 uses the F1 presentation/tracking/build path with a new source and local lighting.
public static class FigureSurface {
  static string Folder => FigureBuild.Folder;
  static string Model => Folder + "/F3_chupacabras_superficie_r05.fbx";
  [Serializable] class Manifest { public int triangles; }
  public static int Triangles => JsonUtility.FromJson<Manifest>(File.ReadAllText(Folder + "/manifest.json")).triangles;
  public static void Configure() {
    ExchangeBuild.Require(!File.Exists(FigureBuild.Scene) && !File.Exists(Folder + "/Figure.prefab"), "Preserve F4 delivery");
    var importer = (ModelImporter)AssetImporter.GetAtPath(Model);
    importer.globalScale = 1; importer.useFileScale = true; importer.bakeAxisConversion = true;
    importer.animationType = ModelImporterAnimationType.None; importer.importAnimation = false;
    importer.importCameras = false; importer.importLights = false; importer.importBlendShapes = false;
    importer.materialImportMode = ModelImporterMaterialImportMode.None;
    importer.importNormals = ModelImporterNormals.Import;
    importer.importTangents = ModelImporterTangents.CalculateMikk;
    importer.meshCompression = ModelImporterMeshCompression.Off; importer.isReadable = false;
    importer.SaveAndReimport();
    foreach (string name in new[] { "BaseColor", "Normal", "MetallicSmoothness" }) {
      var texture = (TextureImporter)AssetImporter.GetAtPath(Folder + "/" + name + ".png");
      texture.textureType = name == "Normal" ? TextureImporterType.NormalMap : TextureImporterType.Default;
      texture.sRGBTexture = name == "BaseColor"; texture.mipmapEnabled = true;
      texture.maxTextureSize = 2048; texture.isReadable = false;
      texture.wrapMode = TextureWrapMode.Clamp; texture.filterMode = FilterMode.Trilinear;
      texture.alphaSource = name == "MetallicSmoothness" ? TextureImporterAlphaSource.FromInput : TextureImporterAlphaSource.None;
      texture.textureCompression = TextureImporterCompression.CompressedHQ;
      texture.SetPlatformTextureSettings(new TextureImporterPlatformSettings {
        name = "Android", overridden = true, maxTextureSize = 2048,
        format = TextureImporterFormat.ASTC_6x6, compressionQuality = 100
      });
      texture.SaveAndReimport();
    }
    var material = new Material(Shader.Find("Universal Render Pipeline/Lit"));
    material.SetColor("_BaseColor", Color.white);
    material.SetTexture("_BaseMap", AssetDatabase.LoadAssetAtPath<Texture2D>(Folder + "/BaseColor.png"));
    material.SetTexture("_BumpMap", AssetDatabase.LoadAssetAtPath<Texture2D>(Folder + "/Normal.png"));
    material.SetTexture("_MetallicGlossMap", AssetDatabase.LoadAssetAtPath<Texture2D>(Folder + "/MetallicSmoothness.png"));
    material.SetFloat("_BumpScale", 1); material.SetFloat("_Smoothness", 1);
    material.SetFloat("_SmoothnessTextureChannel", 0); material.SetFloat("_Metallic", 0);
    material.EnableKeyword("_NORMALMAP"); material.EnableKeyword("_METALLICSPECGLOSSMAP");
    AssetDatabase.CreateAsset(material, Folder + "/Surface.mat");
    EditorSceneManager.OpenScene("Assets/Scenes/F1_FiguraAR_r01.unity");
    var probe = UnityEngine.Object.FindFirstObjectByType<TrackingProbe>();
    var root = probe.staticFigure.gameObject;
    PrefabUtility.UnpackPrefabInstance(root, PrefabUnpackMode.Completely, InteractionMode.AutomatedAction);
    var old = root.transform.Find("StaticFigure");
    var figure = (GameObject)PrefabUtility.InstantiatePrefab(AssetDatabase.LoadAssetAtPath<GameObject>(Model), root.transform);
    figure.name = "StaticFigure";
    figure.transform.localPosition = old.localPosition;
    figure.transform.localRotation = old.localRotation;
    figure.transform.localScale = old.localScale;
    UnityEngine.Object.DestroyImmediate(old.gameObject);
    foreach (var renderer in figure.GetComponentsInChildren<Renderer>(true)) {
      renderer.sharedMaterial = material;
      renderer.shadowCastingMode = ShadowCastingMode.Off; renderer.receiveShadows = false;
    }
    var key = root.transform.Find("FigureKey").GetComponent<Light>();
    key.type = LightType.Directional; key.color = new Color(1, .94f, .84f); key.intensity = 1.5f;
    key.transform.localRotation = figure.transform.localRotation * Quaternion.LookRotation(SourcePoint(new Vector3(-3,-4,-6))); key.shadows = LightShadows.None;
    var fill = root.transform.Find("FigureFill").GetComponent<Light>();
    fill.type = LightType.Directional; fill.color = new Color(.8f, .88f, 1); fill.intensity = .65f;
    fill.transform.localRotation = figure.transform.localRotation * Quaternion.LookRotation(SourcePoint(new Vector3(4,-1,-3))); fill.shadows = LightShadows.None;
    key.cullingMask = fill.cullingMask = 1;
    var pipeline = UnityEngine.Object.Instantiate(probe.figurePipeline);
    pipeline.name = "FigureURP";
    ExchangeBuild.Require(pipeline.additionalLightsRenderingMode == LightRenderingMode.PerPixel, "Per-pixel fill inherited");
    AssetDatabase.CreateAsset(pipeline, Folder + "/FigureURP.asset");
    probe.figurePipeline = pipeline;
    RenderSettings.ambientMode = AmbientMode.Flat; RenderSettings.ambientLight = new Color(.45f,.45f,.45f);
    RenderSettings.skybox = null; RenderSettings.fog = false;
    PrefabUtility.SaveAsPrefabAssetAndConnect(root, Folder + "/Figure.prefab", InteractionMode.AutomatedAction);
    AssetDatabase.SaveAssets();
    EditorSceneManager.SaveScene(probe.gameObject.scene, FigureBuild.Scene);
  }
  public static void VerifyViews(TrackingProbe probe, Camera view) {
    var figure = probe.staticFigure.Find("StaticFigure");
    var meshes = figure.GetComponentsInChildren<MeshFilter>();
    ExchangeBuild.Require(meshes.Length == 1 && meshes[0].sharedMesh.subMeshCount == 1, "One mesh/submesh");
    var mesh = meshes[0].sharedMesh;
    ExchangeBuild.Require(mesh.uv.Length == mesh.vertexCount && mesh.tangents.Length == mesh.vertexCount, "UV/tangents imported");
    ExchangeBuild.Require(mesh.normals.All(n => Mathf.Abs(n.magnitude-1) < .001f), "Unit normals");
    var points = mesh.vertices.Select(v => figure.InverseTransformPoint(meshes[0].transform.TransformPoint(v))).ToArray();
    var bounds = new Bounds(points[0], Vector3.zero);
    foreach (var point in points) bounds.Encapsulate(point);
    Debug.Log("F4_MODEL_BOUNDS local=" + mesh.bounds + " root=" + bounds);
    ExchangeBuild.Require(Mathf.Abs(bounds.size.z - 2.65428f) < .0001f &&
      Mathf.Abs(bounds.size.y - 4.74171f) < .0001f && Mathf.Abs(bounds.max.z) < .0001f, "Meter scale and axis conversion " + bounds);
    ExchangeBuild.Require(AssetDatabase.LoadAllAssetsAtPath(Model).OfType<AnimationClip>().Count() == 0, "No animation clips");
    var renderer = meshes[0].GetComponent<Renderer>();
    var material = renderer.sharedMaterial;
    foreach (string name in new[] { "_BaseMap", "_BumpMap", "_MetallicGlossMap" })
      ExchangeBuild.Require(material.GetTexture(name) != null, "Missing map " + name);
    ExchangeBuild.Require(material.IsKeywordEnabled("_NORMALMAP") && material.IsKeywordEnabled("_METALLICSPECGLOSSMAP"), "PBR keywords");
    foreach (string name in new[] { "BaseColor", "Normal", "MetallicSmoothness" }) {
      var texture = (TextureImporter)AssetImporter.GetAtPath(Folder + "/" + name + ".png");
      ExchangeBuild.Require(!texture.isReadable && texture.mipmapEnabled && texture.sRGBTexture == (name == "BaseColor"), "Texture import " + name);
      ExchangeBuild.Require(texture.GetPlatformTextureSettings("Android").format == TextureImporterFormat.ASTC_6x6, "ASTC " + name);
    }
    var marker = GameObject.Find("Marker_ONLY_FOR_VERIFICATION"); marker.SetActive(false);
    view.orthographic = true; view.aspect = 1100f/850; view.backgroundColor = new Color(.16f,.18f,.21f);
    foreach (var entry in new[] {
      ("frente", new Vector3(0,8,2.1f), new Vector3(0,-.5f,1.2f), 5.5f),
      ("perfil", new Vector3(8,0,2.1f), new Vector3(0,-.5f,1.2f), 5.5f),
      ("espalda", new Vector3(0,-8,2.1f), new Vector3(0,-.5f,1.2f), 5.5f),
      ("tres_cuartos", new Vector3(5,7,3.5f), new Vector3(0,-.5f,1.2f), 5.5f),
      ("inferior", new Vector3(4,5,-1.6f), new Vector3(0,-.15f,1), 4.9f),
      ("rostro", new Vector3(2.1f,5,2), new Vector3(0,.95f,1.38f), 1.65f) }) {
      view.transform.position = figure.TransformPoint(SourcePoint(entry.Item2));
      view.transform.LookAt(figure.TransformPoint(SourcePoint(entry.Item3)), figure.TransformDirection(Vector3.back));
      view.orthographicSize = entry.Item4 * figure.lossyScale.x / (2 * view.aspect);
      Save(view, FigureBuild.Evidence + "/surface_" + entry.Item1 + ".png");
      if (entry.Item1 == "tres_cuartos") {
        foreach (var bg in new[] { ("claro", .8f), ("oscuro", .04f) }) {
          view.backgroundColor = new Color(bg.Item2,bg.Item2,bg.Item2);
          Save(view, FigureBuild.Evidence + "/background_" + bg.Item1 + ".png");
        }
        view.backgroundColor = new Color(.16f,.18f,.21f);
      }
    }
    File.WriteAllText(FigureBuild.Evidence + "/surface_checks.json", JsonUtility.ToJson(new Result {
      triangles = mesh.triangles.Length/3, vertices = mesh.vertexCount, bounds = bounds.size,
      position = figure.localPosition, scale = figure.localScale, rotation = figure.localEulerAngles
    }, true) + "\n");
  }
  // This FBX keeps Blender XY in the mesh and negates Z; F1's root places it on the tag.
  static Vector3 SourcePoint(Vector3 value) => new Vector3(value.x,value.y,-value.z);
  public static void Save(Camera view, string path, int width = 1100, int height = 850) {
    ExchangeBuild.Require(!File.Exists(path), "Preserve capture " + path);
    var target = new RenderTexture(width,height,24);
    var previous = RenderTexture.active;
    view.targetTexture = target;
    // First render after a pipeline switch initializes URP resources; capture the settled frame.
    view.Render(); view.Render(); RenderTexture.active = target;
    var image = new Texture2D(width,height,TextureFormat.RGB24,false);
    image.ReadPixels(new Rect(0,0,width,height),0,0); image.Apply();
    File.WriteAllBytes(path,image.EncodeToPNG());
    view.targetTexture = null; RenderTexture.active = previous;
    UnityEngine.Object.DestroyImmediate(image); target.Release(); UnityEngine.Object.DestroyImmediate(target);
  }
  [Serializable] class Result {
    public bool passed = true, physicalDevice = false;
    public int triangles, vertices, meshes = 1, materials = 1, views = 6;
    public Vector3 bounds, position, scale, rotation;
    public string normalConvention = "MikkTSpace +Y; imported normals", lighting = "Two directional lights, flat neutral ambient, no shadows/sky/environment";
  }
}
