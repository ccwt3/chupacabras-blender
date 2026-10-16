using System.IO;
using System.Linq;
using UnityEditor;
using UnityEditor.Animations;
using UnityEngine;

// F7: change only the controller on the existing R08 character; keep mesh/materials.
public static class FigureBreathingRevision {
  const string Folder = "Assets/FiguraAR/Nocturno_r08_respira_r02";
  public static void Configure() {
    TrackingBuild.RequireVersion();
    string model = Folder + "/chupacabras_nocturno_r08_respira_r02.fbx";
    var importer = (ModelImporter)AssetImporter.GetAtPath(model);
    importer.globalScale = 1; importer.useFileScale = true; importer.bakeAxisConversion = true;
    importer.animationType = ModelImporterAnimationType.Generic; importer.importAnimation = true;
    importer.importCameras = false; importer.importLights = false;
    importer.materialImportMode = ModelImporterMaterialImportMode.None;
    importer.animationCompression = ModelImporterAnimationCompression.Off;
    importer.SaveAndReimport();
    var clips = importer.defaultClipAnimations;
    ExchangeBuild.Require(clips.Length == 1, "One breathing clip");
    foreach (var c in clips) {
      c.name = "Respiracion_4s_R02"; c.loopTime = true; c.loopPose = false;
      c.keepOriginalPositionXZ = true; c.keepOriginalPositionY = true; c.keepOriginalOrientation = true;
      c.lockRootPositionXZ = true; c.lockRootHeightY = true; c.lockRootRotation = true;
    }
    importer.clipAnimations = clips; importer.SaveAndReimport();
    ExchangeBuild.Require(!File.Exists(Folder + "/Respiracion.anim"), "Preserve breathing revision");
    var clip = Object.Instantiate(ExchangeBuild.Clip(model));
    clip.name = "Respiracion_4s_R02";
    foreach (var binding in AnimationUtility.GetCurveBindings(clip))
      if (binding.path.Length == 0) AnimationUtility.SetEditorCurve(clip, binding, null);
    ExchangeBuild.Require(Mathf.Abs(clip.length - 4) < .01f && clip.isLooping, "Four second loop");
    AssetDatabase.CreateAsset(clip, Folder + "/Respiracion.anim");
    var controller = AnimatorController.CreateAnimatorControllerAtPath(Folder + "/Respiracion.controller");
    controller.layers[0].stateMachine.defaultState = controller.layers[0].stateMachine.AddState("Respiracion");
    controller.layers[0].stateMachine.defaultState.motion = clip;
    var root = PrefabUtility.LoadPrefabContents("Assets/FiguraAR/F4_r02/Figure.prefab");
    try {
      root.transform.Find("StaticFigure").GetComponent<Animator>().runtimeAnimatorController = controller;
      PrefabUtility.SaveAsPrefabAsset(root, "Assets/FiguraAR/F4_r02/Figure.prefab");
    } finally { PrefabUtility.UnloadPrefabContents(root); }
    AssetDatabase.SaveAssets();
  }
}
