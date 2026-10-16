using System;
using System.IO;
using System.Linq;
using System.Reflection;
using Chupacabras;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.Playables;

[InitializeOnLoad]
public static class FigurePreview {
  const string Active = "Chupacabras.FigurePreview";
  static double started, phaseStart;
  static int phase, figureId;
  static bool screenshotRequested;
  static Vector3 scale, characterScale;
  static Quaternion characterRotation;
  static bool frozen;
  static int frozenState;
  static float frozenTime;
  static float chestMin = float.PositiveInfinity, chestMax = float.NegativeInfinity;
  static readonly string[] States = { "initial", "acquired", "lost", "recovered", "timeout", "fresh", "background", "resumed", "wrong_id", "correct_id", "menu_return", "menu_reopened", "privacy", "privacy_closed" };
  static FigurePreview() { EditorApplication.update += Tick; }
  public static void Capture() {
    TrackingBuild.RequireVersion();
    Directory.CreateDirectory(FigureBuild.Evidence);
    EditorApplication.delayCall += () => {
      EditorSceneManager.OpenScene(FigureBuild.Scene);
      var probe = UnityEngine.Object.FindFirstObjectByType<TrackingProbe>();
      probe.syntheticPreview = true; probe.syntheticBlank = true;
      SessionState.SetBool(Active, true);
      EditorApplication.ExecuteMenuItem("Window/General/Game");
      EditorApplication.EnterPlaymode();
    };
  }
  static void Ready(TrackingProbe probe, bool value) => typeof(TrackingProbe)
    .GetField("ready", BindingFlags.NonPublic | BindingFlags.Instance).SetValue(probe, value);
  static void Tick() {
    if (!SessionState.GetBool(Active, false)) return;
    if (started == 0) started = phaseStart = EditorApplication.timeSinceStartup;
    if (EditorApplication.timeSinceStartup - started > 100) { Finish(1, "Timeout"); return; }
    if (!EditorApplication.isPlaying || Time.frameCount < 2) return;
    var probe = UnityEngine.Object.FindFirstObjectByType<TrackingProbe>();
    if (probe == null) return;
    var chest = probe.staticFigure.GetComponentsInChildren<Transform>(true).FirstOrDefault(t => t.name == "Torax");
    if (chest != null && probe.staticFigure.gameObject.activeInHierarchy) {
      chestMin = Mathf.Min(chestMin, chest.localScale.x); chestMax = Mathf.Max(chestMax, chest.localScale.x);
    }
    if (EditorApplication.timeSinceStartup - phaseStart < 2) return;
    try {
      var animation = probe.staticFigure.GetComponentInChildren<Animator>(true);
      if (animation != null && animation.isInitialized && !probe.IsAtMenu) {
        var state = animation.GetCurrentAnimatorStateInfo(0);
        if (!probe.staticFigure.gameObject.activeInHierarchy) {
          if (frozen) ExchangeBuild.Require(state.fullPathHash == frozenState && Mathf.Abs(state.normalizedTime - frozenTime) < .001f, "Hidden sequence does not advance");
          frozenState = state.fullPathHash; frozenTime = state.normalizedTime; frozen = true;
        } else if (frozen) {
          ExchangeBuild.Require(state.IsName("Ataque") && state.normalizedTime < .35f, "Recovered sequence restarts from grazing");
          frozen = false;
        }
      } else frozen = false;
      string screenshot = Path.Combine(Path.GetFullPath(FigureBuild.Evidence), "interface_" + States[phase] + ".png");
      if (!screenshotRequested) {
        ScreenCapture.CaptureScreenshot(screenshot); screenshotRequested = true; return;
      }
      if (!File.Exists(screenshot)) return;
      if (phase == 0 || phase == 10 || phase == 12 || phase == 13) {
        ExchangeBuild.Require(probe.IsAtMenu, "Welcome screen before camera");
        probe.SendMessage("OnApplicationPause", true);
        probe.SendMessage("OnApplicationPause", false);
        ExchangeBuild.Require(!(bool)typeof(TrackingProbe).GetField("ready", BindingFlags.NonPublic | BindingFlags.Instance).GetValue(probe), "Resume in menu must not open camera");
        ExchangeBuild.Require(typeof(TrackingProbe).GetField("webcam", BindingFlags.NonPublic | BindingFlags.Instance).GetValue(probe) == null, "Menu releases webcam");
      } else ExchangeBuild.Require(!probe.IsAtMenu, "Camera experience entered");
      ExchangeBuild.Require(probe.ShowingPrivacy == (phase == 12), "Privacy screen state");
      bool visible = phase == 1 || phase == 3 || phase == 5 || phase == 7 || phase == 9 || phase == 11;
      ExchangeBuild.Require(probe.State.Visible == visible && probe.staticFigure.gameObject.activeInHierarchy == visible, "Visibility " + States[phase]);
      var character = probe.staticFigure.Find("StaticFigure");
      if (figureId == 0) {
        figureId = probe.staticFigure.GetInstanceID(); scale = probe.staticFigure.lossyScale;
        characterScale = character.localScale; characterRotation = character.localRotation;
      }
      ExchangeBuild.Require(character.localScale == characterScale && character.localRotation == characterRotation &&
        character.localPosition == Vector3.zero, "Animation preserves character placement");
      ExchangeBuild.Require(probe.staticFigure.GetInstanceID() == figureId && probe.staticFigure.lossyScale == scale, "No duplication or scale jump");
      ExchangeBuild.Require(probe.State.PlaybackSeconds == 0, "No narrative clock");
      ExchangeBuild.Require(UnityEngine.Object.FindObjectsByType<Camera>(FindObjectsSortMode.None).Length == 2, "Only AR and clear cameras");
      ExchangeBuild.Require(UnityEngine.Object.FindObjectsByType<AppearanceStudy>(FindObjectsSortMode.None).Length == 0 &&
        UnityEngine.Object.FindObjectsByType<Animator>(FindObjectsSortMode.None).All(a =>
          a.transform.IsChildOf(probe.staticFigure) && a.runtimeAnimatorController != null && !a.applyRootMotion) &&
        UnityEngine.Object.FindObjectsByType<PlayableDirector>(FindObjectsSortMode.None).Length == 0, "No cinematic runtime");
      ExchangeBuild.Require(UnityEngine.Object.FindObjectsByType<Renderer>(FindObjectsSortMode.None).All(r => r.sharedMaterials.All(m => !(m.mainTexture is RenderTexture))), "No cinematic render target");
      var view = GameObject.Find("ARCamera").GetComponent<Camera>();
      var rect = view.rect; view.rect = CameraGeometry.Fit(view.aspect, 960f / 540);
      ExchangeBuild.SaveCamera(view, FigureBuild.Evidence + "/runtime_" + States[phase] + ".png");
      view.rect = rect;
      phase++; screenshotRequested = false;
      if (phase == States.Length) {
        ExchangeBuild.Require(chest == null || chestMax - chestMin > .02f, "Runtime breathing is actually advancing");
        Finish(0, "Initial, acquisition, loss, recovery, camera timeout, fresh frame, background, resume, wrong ID rejected, correct ID recovered; welcome, menu pause/resume, return, reopen and privacy; same figure and scale; restart from grazing after every tracking loss, including completed attack; no cine."); return; }
      if (phase == 1 || phase == 11) probe.BeginExperience();
      if (phase == 10 || phase == 13) probe.ReturnToMenu();
      if (phase == 12) { probe.ShowPrivacy(); probe.BeginExperience(); ExchangeBuild.Require(probe.IsAtMenu, "Privacy does not start camera"); }
      if (phase == 1 || phase == 3) probe.syntheticBlank = false;
      if (phase == 2) {
        // Lose the tag after the completed attack, so resuming the old state cannot pass.
        if (animation != null) { animation.Play("Reposo", 0, .5f); animation.Update(0); }
        probe.syntheticBlank = true;
      }
      if (phase == 4) Ready(probe, false);
      if (phase == 5) Ready(probe, true);
      if (phase == 6) {
        probe.SendMessage("OnApplicationPause", true);
        ExchangeBuild.Require(!probe.staticFigure.gameObject.activeInHierarchy, "Background hides immediately");
      }
      if (phase == 7) probe.SendMessage("OnApplicationPause", false);
      if (phase == 8) {
        var wrong = new Texture2D(2, 2);
        ExchangeBuild.Require(wrong.LoadImage(File.ReadAllBytes("docs/fixtures/tag41h12_id1.png")), "Load wrong-ID fixture");
        using (var detector = new AprilTag.TagDetector(wrong.width, wrong.height, 2)) {
          detector.ProcessImage(wrong.GetPixels32(), 60 * Mathf.Deg2Rad, .1f);
          var tags = detector.DetectedTags.ToArray();
          ExchangeBuild.Require(tags.Length == 1 && tags[0].ID == 1, "Fixture really detects ID 1");
        }
        probe.syntheticFixture = wrong;
      }
      if (phase == 9) {
        UnityEngine.Object.Destroy(probe.syntheticFixture);
        probe.syntheticFixture = null;
      }
      phaseStart = EditorApplication.timeSinceStartup;
    } catch (Exception e) { Finish(1, e.ToString()); }
  }
  static void Finish(int code, string message) {
    File.WriteAllText(FigureBuild.Evidence + "/runtime.json", JsonUtility.ToJson(new Result { passed = code == 0, detail = message }, true));
    Debug.Log("CHUPACABRAS_FIGURE_RUNTIME " + message);
    SessionState.SetBool(Active, false);
    EditorApplication.Exit(code);
  }
  [Serializable] class Result { public bool passed; public bool physicalDevice = false; public string detail; }
}
