using System;
using System.IO;
using System.Linq;
using Chupacabras;
using UnityEditor;
using UnityEditor.Animations;
using UnityEngine;
using UnityEngine.Rendering;

// Only the character child of the existing presentation prefab is replaced.
public static class FigureNocturno {
  public const string Folder = "Assets/FiguraAR/Nocturno_r08";
  const string Model = Folder + "/chupacabras_nocturno_r08.fbx";
  const string Prefab = "Assets/FiguraAR/F4_r02/Figure.prefab";
  [Serializable] class Manifest { public int triangles; }
  public static int Triangles => JsonUtility.FromJson<Manifest>(File.ReadAllText(Folder + "/manifest.json")).triangles;
  public static bool IsBreathing(Transform root) => root.GetComponentsInChildren<SkinnedMeshRenderer>(true).Length == 1;
  public static void Configure() {
    TrackingBuild.RequireVersion();
    var importer = (ModelImporter)AssetImporter.GetAtPath(Model);
    importer.globalScale = 1; importer.useFileScale = true; importer.bakeAxisConversion = true;
    importer.animationType = ModelImporterAnimationType.Generic; importer.importAnimation = true;
    importer.importCameras = false; importer.importLights = false; importer.importBlendShapes = false;
    importer.materialImportMode = ModelImporterMaterialImportMode.None;
    importer.importNormals = ModelImporterNormals.Import;
    importer.importTangents = ModelImporterTangents.CalculateMikk;
    importer.meshCompression = ModelImporterMeshCompression.Off; importer.isReadable = false;
    importer.animationCompression = ModelImporterAnimationCompression.Off;
    importer.SaveAndReimport();
    var clips = importer.defaultClipAnimations;
    ExchangeBuild.Require(clips.Length == 1, "One breathing clip");
    foreach (var c in clips) {
      c.name = "Respiracion_4s"; c.loopTime = true; c.loopPose = false;
      c.keepOriginalPositionXZ = true; c.keepOriginalPositionY = true; c.keepOriginalOrientation = true;
      c.lockRootPositionXZ = true; c.lockRootHeightY = true; c.lockRootRotation = true;
    }
    importer.clipAnimations = clips; importer.SaveAndReimport();
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
    ExchangeBuild.Require(!File.Exists(Folder + "/Surface.mat"), "Preserve existing revision");
    var material = new Material(Shader.Find("Universal Render Pipeline/Lit"));
    material.SetColor("_BaseColor", Color.white);
    material.SetTexture("_BaseMap", AssetDatabase.LoadAssetAtPath<Texture2D>(Folder + "/BaseColor.png"));
    material.SetTexture("_BumpMap", AssetDatabase.LoadAssetAtPath<Texture2D>(Folder + "/Normal.png"));
    material.SetTexture("_MetallicGlossMap", AssetDatabase.LoadAssetAtPath<Texture2D>(Folder + "/MetallicSmoothness.png"));
    material.SetFloat("_BumpScale", 1); material.SetFloat("_Smoothness", 1);
    material.SetFloat("_SmoothnessTextureChannel", 0); material.SetFloat("_Metallic", 0);
    material.EnableKeyword("_NORMALMAP"); material.EnableKeyword("_METALLICSPECGLOSSMAP");
    AssetDatabase.CreateAsset(material, Folder + "/Surface.mat");
    var controller = AnimatorController.CreateAnimatorControllerAtPath(Folder + "/Respiracion.controller");
    var state = controller.layers[0].stateMachine.AddState("Respiracion"); state.motion = CreateBreathingClip();
    controller.layers[0].stateMachine.defaultState = state;
    var root = PrefabUtility.LoadPrefabContents(Prefab);
    try {
      var old = root.transform.Find("StaticFigure");
      var figure = (GameObject)PrefabUtility.InstantiatePrefab(AssetDatabase.LoadAssetAtPath<GameObject>(Model), root.transform);
      figure.name = "StaticFigure";
      figure.transform.localPosition = old.localPosition;
      figure.transform.localRotation = old.localRotation;
      figure.transform.localScale = old.localScale;
      var animator = figure.GetComponent<Animator>();
      if (animator == null) animator = figure.AddComponent<Animator>();
      animator.runtimeAnimatorController = controller; animator.applyRootMotion = false;
      animator.cullingMode = AnimatorCullingMode.AlwaysAnimate;
      foreach (var renderer in figure.GetComponentsInChildren<SkinnedMeshRenderer>(true)) {
        renderer.sharedMaterial = material;
        renderer.shadowCastingMode = ShadowCastingMode.Off; renderer.receiveShadows = false;
        // Bounds include the full authored breath/tail cycle, also when the marker reappears.
        var bounds = renderer.localBounds; bounds.Expand(.12f); renderer.localBounds = bounds;
      }
      UnityEngine.Object.DestroyImmediate(old.gameObject);
      PrefabUtility.SaveAsPrefabAsset(root, Prefab);
    } finally { PrefabUtility.UnloadPrefabContents(root); }
    AssetDatabase.SaveAssets();
    Debug.Log("NOCTURNO_CHARACTER_REPLACED");
  }
  static AnimationClip BreathingClip => AssetDatabase.LoadAssetAtPath<AnimationClip>(Folder + "/Respiracion.anim");
  static AnimationClip CreateBreathingClip() {
    if (BreathingClip != null) return BreathingClip;
    var clip = UnityEngine.Object.Instantiate(ExchangeBuild.Clip(Model));
    clip.name = "Respiracion_4s";
    // FBX bakes constant transforms on the model root too. Only bones may animate:
    // empty-path curves would overwrite the existing presentation's scale/rotation.
    foreach (var binding in AnimationUtility.GetCurveBindings(clip))
      if (binding.path.Length == 0) AnimationUtility.SetEditorCurve(clip, binding, null);
    AssetDatabase.CreateAsset(clip, Folder + "/Respiracion.anim");
    return clip;
  }
  public static void ConfigureBreathingClip() {
    var controller = AssetDatabase.LoadAssetAtPath<AnimatorController>(Folder + "/Respiracion.controller");
    controller.layers[0].stateMachine.defaultState.motion = CreateBreathingClip();
    EditorUtility.SetDirty(controller); AssetDatabase.SaveAssets();
  }
  public static void VerifyViews(TrackingProbe probe, Camera view) {
    var figure = probe.staticFigure.Find("StaticFigure");
    var renderer = figure.GetComponentInChildren<SkinnedMeshRenderer>();
    var animator = figure.GetComponent<Animator>();
    var mesh = renderer.sharedMesh;
    ExchangeBuild.Require(mesh.triangles.Length / 3 == Triangles && Triangles < 130000, "Character triangle budget");
    ExchangeBuild.Require(mesh.subMeshCount == 1 && renderer.sharedMaterials.Length == 1 && renderer.bones.Length <= 4, "One material and compact skeleton");
    ExchangeBuild.Require(mesh.uv.Length == mesh.vertexCount && mesh.tangents.Length == mesh.vertexCount, "UV and tangent coverage");
    ExchangeBuild.Require(animator != null && !animator.applyRootMotion && animator.runtimeAnimatorController != null, "Local breathing controller");
    var clip = animator.runtimeAnimatorController.animationClips.Single();
    ExchangeBuild.Require(Mathf.Abs(clip.length - 4) < .01f && clip.isLooping, "Four second loop");
    foreach (string property in new[] { "_BaseMap", "_BumpMap", "_MetallicGlossMap" })
      ExchangeBuild.Require(renderer.sharedMaterial.GetTexture(property) != null, "Character texture " + property);
    ExchangeBuild.Require(AnimationUtility.GetCurveBindings(clip).All(b => b.path.Length > 0), "No presentation/root transform curves");
    var originalScale = figure.localScale; var originalRotation = figure.localRotation;
    var baked = new Mesh();
    clip.SampleAnimation(figure.gameObject, 0); renderer.BakeMesh(baked, true);
    var rest = baked.vertices;
    clip.SampleAnimation(figure.gameObject, 2); renderer.BakeMesh(baked, true);
    var inhale = baked.vertices;
    clip.SampleAnimation(figure.gameObject, 4); renderer.BakeMesh(baked, true);
    var loop = baked.vertices;
    ExchangeBuild.Require(figure.localScale == originalScale && figure.localRotation == originalRotation, "Animation preserves presentation transform");
    float movement = rest.Select((v, i) => Vector3.Distance(v, inhale[i])).Max();
    float seam = rest.Select((v, i) => Vector3.Distance(v, loop[i])).Max();
    bool revised = clip.name == "Respiracion_4s_R02";
    ExchangeBuild.Require(movement > (revised ? .12f : .01f) && movement < (revised ? .20f : .15f) && seam < .0001f, "Breathing deformation and seamless loop " + movement + "/" + seam);
    // Measure support in presentation coordinates; the existing prefab's orientation is preserved.
    var worldRest = rest.Select(v => figure.InverseTransformPoint(renderer.transform.TransformPoint(v))).ToArray();
    var bounds = new Bounds(worldRest[0], Vector3.zero);
    foreach (var p in worldRest) bounds.Encapsulate(p);
    ExchangeBuild.Require(bounds.size.x > 2 && bounds.size.x < 2.6f &&
      bounds.size.y > 4.4f && bounds.size.y < 5 && bounds.size.z > 2.3f && bounds.size.z < 2.9f &&
      Mathf.Abs(bounds.max.z) < .003f, "Authored meter scale, axes and support " + bounds);
    float support = worldRest.Max(v => v.z);
    var feet = Enumerable.Range(0, rest.Length).Where(i => worldRest[i].z > support - .15f).ToArray();
    float drift = feet.Max(i => Vector3.Distance(rest[i], inhale[i]));
    ExchangeBuild.Require(feet.Length > 30 && drift < .0001f, "Planted feet " + drift);
    UnityEngine.Object.DestroyImmediate(baked);
    clip.SampleAnimation(figure.gameObject, 0);
    var marker = GameObject.Find("Marker_ONLY_FOR_VERIFICATION"); if (marker) marker.SetActive(false);
    view.orthographic = true; view.aspect = 1100f/850; view.backgroundColor = new Color(.16f,.18f,.21f);
    foreach (var entry in new[] {
      ("frente", new Vector3(0,8,2.1f), new Vector3(0,-.5f,1.2f), 5.5f),
      ("perfil", new Vector3(8,0,2.1f), new Vector3(0,-.5f,1.2f), 5.5f),
      ("espalda", new Vector3(0,-8,2.1f), new Vector3(0,-.5f,1.2f), 5.5f),
      ("tres_cuartos", new Vector3(5,7,3.5f), new Vector3(0,-.5f,1.2f), 5.5f),
      ("rostro", new Vector3(2.1f,5,2), new Vector3(0,.95f,1.4f), 1.9f) }) {
      view.transform.position = figure.TransformPoint(new Vector3(entry.Item2.x,entry.Item2.y,-entry.Item2.z));
      view.transform.LookAt(figure.TransformPoint(new Vector3(entry.Item3.x,entry.Item3.y,-entry.Item3.z)), figure.TransformDirection(Vector3.back));
      view.orthographicSize = entry.Item4 * figure.lossyScale.x / (2 * view.aspect);
      FigureSurface.Save(view, FigureBuild.Evidence + "/nocturno_" + entry.Item1 + ".png");
    }
    File.WriteAllText(FigureBuild.Evidence + "/character_checks.json", JsonUtility.ToJson(new Result {
      triangles = Triangles, vertices = mesh.vertexCount, maxMotion = movement, loopSeam = seam, footDrift = drift
    }, true));
  }
  [Serializable] class Result {
    public bool passed = true, physicalDevice = false;
    public int triangles, vertices;
    public float maxMotion, loopSeam, footDrift;
  }
}
