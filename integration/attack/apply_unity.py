"""Historical one-shot installer for 0.2.5; do not rerun for later revisions."""
from pathlib import Path
import shutil
import json
ROOT=Path(__file__).resolve().parents[2]
PROJECT=Path('/home/cacawatin/code/unity/chupacabras/google_play')
assert (PROJECT/'.google-play-copy').exists()
evidence=PROJECT/'docs/evidencias/ataque_20261011'
evidence.mkdir(exist_ok=False)
backup=evidence/'sources_before';backup.mkdir()
files=['Assets/Editor/FigureBuild.cs','Assets/Editor/GooglePlayBuild.cs','Assets/Editor/FigurePreview.cs','Assets/Scripts/TrackingProbe.cs','scripts/verify_google_play.py','scripts/verify_figure_apk.py','Assets/Resources/ThirdPartyNotices.txt']
for name in files:
 p=PROJECT/name
 shutil.copy2(p,backup/p.name)
 if name.endswith(('FigureBuild.cs','GooglePlayBuild.cs','verify_google_play.py','verify_figure_apk.py')):
  text=p.read_text().replace('0.2.4','0.2.5').replace('204','205')
  p.write_text(text)
p=PROJECT/'Assets/Editor/FigureBuild.cs';s=p.read_text()
s=s.replace('public static string Scene => "Assets/Scenes/"','public static string Scene => AttackBuild.IsConfigured ? AttackBuild.Scene : "Assets/Scenes/"')
s=s.replace('public static void Verify() {','public static void Verify() {\n    if (AttackBuild.IsConfigured) { AttackBuild.Verify(); return; }')
s=s.replace('p.Contains("chupacabras_nocturno"))','p.Contains("chupacabras_nocturno") || p.Contains("ataque_ar"))')
p.write_text(s)
p=PROJECT/'Assets/Scripts/TrackingProbe.cs';s=p.read_text()
s=s.replace('cameraRequested = true;\n            Screen.sleepTimeout', 'if (IsAtMenu) staticFigure.GetComponentInChildren<AttackPlayback>(true)?.RestartSequence();\n            cameraRequested = true;\n            Screen.sleepTimeout')
s=s.replace('Chupacabras sobre el marcador','Chupacabras y oveja sobre el marcador')
s=s.replace('Una figura en realidad aumentada','Una escena en realidad aumentada').replace('Apunta la cámara y muévete para explorar la figura.','Apunta la cámara para ver al chupacabras y la oveja en 3D.')
p.write_text(s)
p=PROJECT/'Assets/Editor/FigurePreview.cs';s=p.read_text()
s=s.replace('static float chestMin', 'static bool frozen;\n  static int frozenState;\n  static float frozenTime;\n  static float chestMin')
s=s.replace('string screenshot =', """var animation = probe.staticFigure.GetComponentInChildren<Animator>(true);
      if (animation != null && animation.isInitialized && !probe.IsAtMenu) {
        var state = animation.GetCurrentAnimatorStateInfo(0);
        if (!probe.staticFigure.gameObject.activeInHierarchy) {
          if (frozen) ExchangeBuild.Require(state.fullPathHash == frozenState && Mathf.Abs(state.normalizedTime - frozenTime) < .001f, "Hidden sequence does not advance");
          frozenState = state.fullPathHash; frozenTime = state.normalizedTime; frozen = true;
        } else if (frozen) {
          ExchangeBuild.Require(state.fullPathHash != frozenState || state.normalizedTime >= frozenTime, "Recovered sequence does not restart");
          frozen = false;
        }
      } else frozen = false;
      string screenshot =""")
p.write_text(s)
for name,dest in [('AttackBuild.cs','Assets/Editor'),('AttackPlayback.cs','Assets/Scripts')]:
 target=PROJECT/dest/name;assert not target.exists();shutil.copy2(ROOT/'integration/attack'/name,target)
folder=PROJECT/'Assets/FiguraAR/Ataque_r02';folder.mkdir(exist_ok=False)
for ext in ('.fbx','.json'):shutil.copy2(ROOT/'exports'/('ataque_ar_r02'+ext),folder)
p=PROJECT/'Assets/Resources/ThirdPartyNotices.txt'
p.write_text(p.read_text()+'\nOveja adaptada de Farm Animals Pack, Quaternius (2018). CC0 1.0.\nhttps://quaternius.com/packs/farmanimal.html\nhttps://creativecommons.org/publicdomain/zero/1.0/\n')
shutil.copy2(ROOT/'historicos/assets/oveja/original/Farm Animals by @Quaternius/License.txt',folder/'SheepLicense.txt')
print('Attack installed into',PROJECT)
