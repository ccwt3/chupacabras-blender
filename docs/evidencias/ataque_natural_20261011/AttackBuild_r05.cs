using System;
using System.IO;
using System.Linq;
using Chupacabras;
using UnityEditor;
using UnityEditor.Animations;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.Animations;
using UnityEngine.Playables;
using UnityEngine.Rendering;
using UnityEngine.Rendering.Universal;

public static class AttackBuild {
    public const string Folder = "Assets/FiguraAR/Ataque_r05";
    public const string Scene = "Assets/Scenes/AtaqueAR_r05.unity";
    const string Model = Folder + "/ataque_ar_r05.fbx";
    public static bool IsConfigured => File.Exists(Scene);
    public static void Configure() {
        TrackingBuild.RequireVersion(); GooglePlayBuild.RequireCopy();
        ExchangeBuild.Require(!IsConfigured, "Preserve existing attack revision");
        AssetDatabase.Refresh();
        var importer = (ModelImporter)AssetImporter.GetAtPath(Model);
        importer.globalScale = 1; importer.useFileScale = true; importer.bakeAxisConversion = true;
        importer.animationType = ModelImporterAnimationType.Generic; importer.importAnimation = true;
        importer.importCameras = false; importer.importLights = false;
        importer.materialImportMode = ModelImporterMaterialImportMode.None;
        importer.animationCompression = ModelImporterAnimationCompression.Off;
        importer.meshCompression = ModelImporterMeshCompression.Off;
        importer.importNormals = ModelImporterNormals.Import; importer.importTangents = ModelImporterTangents.CalculateMikk;
        importer.SaveAndReimport();
        var source = importer.defaultClipAnimations.Single();
        importer.clipAnimations = new[] { Clip(source.takeName,"Ataque",1,325,false), Clip(source.takeName,"Reposo",325,421,true) };
        importer.SaveAndReimport();
        var clips = AssetDatabase.LoadAllAssetsAtPath(Model).OfType<AnimationClip>().Where(c=>!c.name.StartsWith("__")).ToArray();
        var controller = AnimatorController.CreateAnimatorControllerAtPath(Folder+"/Ataque.controller");
        var machine = controller.layers[0].stateMachine;
        var attack = machine.AddState("Ataque"); var idle = machine.AddState("Reposo");
        foreach(var pair in new[] {(state:attack,name:"Ataque"),(state:idle,name:"Reposo")}) {
            var clip = UnityEngine.Object.Instantiate(clips.Single(c=>c.name==pair.name));
            clip.name = pair.name;
            foreach(var binding in AnimationUtility.GetCurveBindings(clip))
                if(binding.path.Length==0) AnimationUtility.SetEditorCurve(clip,binding,null);
            AssetDatabase.CreateAsset(clip,Folder+"/"+pair.name+".anim"); pair.state.motion=clip;
        }
        machine.defaultState = attack;
        var transition = attack.AddTransition(idle); transition.hasExitTime=true;transition.exitTime=1;
        transition.hasFixedDuration=true;transition.duration=0;
        var presentation = PrefabUtility.LoadPrefabContents("Assets/FiguraAR/F4_r02/Figure.prefab");
        try {
            var old=presentation.transform.Find("StaticFigure");
            var placement=new GameObject("StaticFigure").transform;placement.SetParent(presentation.transform,false);
            placement.localPosition=old.localPosition;placement.localRotation=old.localRotation;placement.localScale=old.localScale;
            var model=(GameObject)PrefabUtility.InstantiatePrefab(AssetDatabase.LoadAssetAtPath<GameObject>(Model),placement);
            // The multi-actor FBX retains its axis-conversion node beneath the model root.
            model.transform.localRotation=Quaternion.Euler(-90,0,0);
            foreach(var a in model.GetComponentsInChildren<Animator>()) UnityEngine.Object.DestroyImmediate(a);
            var animator=model.AddComponent<Animator>();animator.runtimeAnimatorController=controller;
            animator.applyRootMotion=false;animator.cullingMode=AnimatorCullingMode.AlwaysAnimate;
            animator.keepAnimatorStateOnDisable=true;model.AddComponent<AttackPlayback>();
            var wool=Material("Lana",new Color(.78f,.75f,.64f));
            var skin=Material("OvejaPiel",new Color(.10f,.075f,.055f));
            foreach(var renderer in model.GetComponentsInChildren<SkinnedMeshRenderer>()) {
                renderer.sharedMaterials=renderer.name.Contains("Sheep")?new[]{wool,skin}:new[]{AssetDatabase.LoadAssetAtPath<Material>(FigureNocturno.Folder+"/Surface.mat")};
                renderer.shadowCastingMode=ShadowCastingMode.Off;renderer.receiveShadows=false;
                renderer.updateWhenOffscreen=true;
            }
            FitToMarker(presentation.transform, placement, animator);
            UnityEngine.Object.DestroyImmediate(old.gameObject);
            PrefabUtility.SaveAsPrefabAsset(presentation,Folder+"/Figure.prefab");
        } finally { PrefabUtility.UnloadPrefabContents(presentation); }
        var scene=EditorSceneManager.OpenScene("Assets/Scenes/F4_FiguraAR_r02.unity");
        var probe=UnityEngine.Object.FindFirstObjectByType<TrackingProbe>();
        var previous=probe.staticFigure;
        var replacement=(GameObject)PrefabUtility.InstantiatePrefab(AssetDatabase.LoadAssetAtPath<GameObject>(Folder+"/Figure.prefab"));
        replacement.transform.SetPositionAndRotation(previous.position,previous.rotation);
        replacement.transform.localScale=previous.localScale;
        replacement.SetActive(false);probe.staticFigure=replacement.transform;
        UnityEngine.Object.DestroyImmediate(previous.gameObject);
        EditorSceneManager.SaveScene(scene,Scene);AssetDatabase.SaveAssets();
    }
    [Serializable] class VolumeReport { public Vector3 size,center; public float uniformScale; public int sampleHz; }
    static void FitToMarker(Transform anchor,Transform placement,Animator animator) {
        var bounds=Envelope(anchor,animator);
        float factor=.90f/Mathf.Max(bounds.size.x,bounds.size.y,bounds.size.z);
        placement.localScale*=factor;
        bounds=Envelope(anchor,animator);
        Vector3 shift=new Vector3(-bounds.center.x,-bounds.center.y,-bounds.max.z);
        animator.transform.localPosition+=placement.InverseTransformVector(anchor.TransformVector(shift));
    }
    static Bounds Envelope(Transform anchor,Animator animator) {
        var graph=PlayableGraph.Create("WholeAnimationBounds");
        var skins=animator.GetComponentsInChildren<SkinnedMeshRenderer>(true);
        var mesh=new Mesh();var bounds=new Bounds();bool first=true;
        bool active=anchor.gameObject.activeSelf;anchor.gameObject.SetActive(true);
        try {
            graph.SetTimeUpdateMode(DirectorUpdateMode.Manual);
            var output=AnimationPlayableOutput.Create(graph,"Bounds",animator);graph.Play();
            foreach(string name in new[]{"Ataque","Reposo"}) {
                var clip=AssetDatabase.LoadAssetAtPath<AnimationClip>(Folder+"/"+name+".anim");
                var playable=AnimationClipPlayable.Create(graph,clip);playable.SetApplyFootIK(false);output.SetSourcePlayable(playable);
                for(int sample=0;sample<=Mathf.CeilToInt(clip.length*48);sample++) {
                    playable.SetTime(Mathf.Min(clip.length,sample/48f));graph.Evaluate(0);
                    foreach(var skin in skins) {
                        skin.forceMatrixRecalculationPerRender=true;skin.BakeMesh(mesh,true);
                        var matrix=anchor.worldToLocalMatrix*skin.transform.localToWorldMatrix;
                        foreach(var vertex in mesh.vertices) {
                            var point=matrix.MultiplyPoint3x4(vertex);
                            if(first){bounds=new Bounds(point,Vector3.zero);first=false;}else bounds.Encapsulate(point);
                        }
                    }
                }
            }
            return bounds;
        } finally { graph.Destroy();UnityEngine.Object.DestroyImmediate(mesh);anchor.gameObject.SetActive(active); }
    }
    static Material Material(string name,Color color) {
        var material=new Material(Shader.Find("Universal Render Pipeline/Lit"));
        material.SetColor("_BaseColor",color);material.SetFloat("_Smoothness",.07f);
        AssetDatabase.CreateAsset(material,Folder+"/"+name+".mat");return material;
    }
    static ModelImporterClipAnimation Clip(string take,string name,float start,float end,bool loop) => new ModelImporterClipAnimation {
        takeName=take,name=name,firstFrame=start,lastFrame=end,loopTime=loop,loopPose=false,
        keepOriginalPositionXZ=true,keepOriginalPositionY=true,keepOriginalOrientation=true,
        lockRootPositionXZ=true,lockRootHeightY=true,lockRootRotation=true
    };
    public static void Verify() {
        TrackingBuild.RequireVersion();TrackingChecks.Run();Directory.CreateDirectory(FigureBuild.Evidence);
        EditorSceneManager.OpenScene(Scene);
        var probe=UnityEngine.Object.FindFirstObjectByType<TrackingProbe>();
        ExchangeBuild.Require(probe.appearance==null && !probe.staticFigure.gameObject.activeSelf,"Starts hidden, direct AR");
        var model=probe.staticFigure.Find("StaticFigure");
        var animator=model.GetComponentInChildren<Animator>();
        var skins=model.GetComponentsInChildren<SkinnedMeshRenderer>(true);
        foreach(var skin in skins) skin.forceMatrixRecalculationPerRender=true;
        ExchangeBuild.Require(skins.Length==2 && model.GetComponentsInChildren<Animator>(true).Length==1,"Two actors, one synchronized animator");
        ExchangeBuild.Require(animator.keepAnimatorStateOnDisable && !animator.applyRootMotion,"Pause preserves state and anchor");
        var attack=AssetDatabase.LoadAssetAtPath<AnimationClip>(Folder+"/Ataque.anim");
        var idle=AssetDatabase.LoadAssetAtPath<AnimationClip>(Folder+"/Reposo.anim");
        ExchangeBuild.Require(Mathf.Abs(attack.length-13.5f)<.01f && !attack.isLooping && Mathf.Abs(idle.length-4)<.01f && idle.isLooping,"Grazing, attack, walking return, then four-second rest loop");
        ExchangeBuild.Require(new[]{attack,idle}.All(c=>AnimationUtility.GetCurveBindings(c).All(b=>b.path.Length>0)),"Anchor not animated");
        int triangles=skins.Sum(s=>s.sharedMesh.triangles.Length/3);
        ExchangeBuild.Require(triangles==112822,"Authored geometry imported intact");
        var sheep=skins.Single(s=>s.name.Contains("Sheep"));var creature=skins.Single(s=>!s.name.Contains("Sheep"));
        ExchangeBuild.Require(creature.sharedMaterials.Length==1 && creature.sharedMaterial.GetTexture("_BaseMap")!=null,"R08 appearance preserved");
        string[] dependencies=AssetDatabase.GetDependencies(Scene,true);
        FigureBuild.CheckDependencies(dependencies);File.WriteAllLines(FigureBuild.Evidence+"/scene_dependencies.txt",dependencies.OrderBy(p=>p));
        var envelope = Envelope(probe.staticFigure, animator);
        ExchangeBuild.Require(envelope.min.x>=-.5f && envelope.max.x<=.5f && envelope.min.y>=-.5f && envelope.max.y<=.5f && envelope.min.z>=-1 && envelope.max.z<=.0001f,"Complete animation inside one metre cube: "+envelope);
        ExchangeBuild.Require(Mathf.Abs(model.localScale.x-model.localScale.y)<.00001f && Mathf.Abs(model.localScale.x-model.localScale.z)<.00001f,"Uniform scale preserves both actors' proportions");
        File.WriteAllText(FigureBuild.Evidence+"/volume.json",JsonUtility.ToJson(new VolumeReport { size=envelope.size, center=envelope.center, uniformScale=model.localScale.x, sampleHz=48 },true));
        var previous=QualitySettings.renderPipeline;
        var graph=PlayableGraph.Create("AttackVerification");
        try {
            QualitySettings.renderPipeline=probe.figurePipeline;probe.staticFigure.gameObject.SetActive(true);
            graph.SetTimeUpdateMode(DirectorUpdateMode.Manual);
            var playable=AnimationClipPlayable.Create(graph,attack);playable.SetApplyFootIK(false);
            var output=AnimationPlayableOutput.Create(graph,"Review",animator);output.SetSourcePlayable(playable);
            graph.Play();
            var view=new GameObject("AttackReview").AddComponent<Camera>();view.GetUniversalAdditionalCameraData();
            view.orthographic=true;view.aspect=1.5f;view.nearClipPlane=.001f;view.farClipPlane=10;
            view.clearFlags=CameraClearFlags.SolidColor;view.backgroundColor=new Color(.12f,.14f,.17f);view.cullingMask=1;
            view.transform.position=model.TransformPoint(new Vector3(8,10,-6));
            view.transform.LookAt(model.TransformPoint(new Vector3(0,0,-1)),model.TransformDirection(Vector3.back));
            view.orthographicSize=9f*model.lossyScale.x/2;
            foreach(float t in new[]{0f,2.5f,3f,3.5f,4.5f,7f,8.5f,10f,11.5f,13.5f}) {
                playable.SetTime(t);graph.Evaluate(0);
                FigureSurface.Save(view,FigureBuild.Evidence+"/attack_"+t.ToString("0.0",System.Globalization.CultureInfo.InvariantCulture)+".png",960,640);
            }
            var restPlayable=AnimationClipPlayable.Create(graph,idle);restPlayable.SetApplyFootIK(false);output.SetSourcePlayable(restPlayable);
            restPlayable.SetTime(0);graph.Evaluate(0);var rest=Vertices(sheep);var chupa=Vertices(creature);
            restPlayable.SetTime(2);graph.Evaluate(0);
            float sheepDrift=Difference(rest,Vertices(sheep));float breath=Difference(chupa,Vertices(creature));
            restPlayable.SetTime(4);graph.Evaluate(0);float seam=Difference(chupa,Vertices(creature));
            ExchangeBuild.Require(sheepDrift<.0001f && seam<.0001f && breath>.001f,"Motionless sheep and seamless breathing "+sheepDrift+"/"+seam+"/"+breath);
            File.WriteAllText(FigureBuild.Evidence+"/checks.json","{\"passed\":true,\"physicalDevice\":false,\"triangles\":"+triangles+",\"actors\":2,\"attackSeconds\":13.5,\"restLoopSeconds\":4}\n");
        } finally {graph.Destroy();QualitySettings.renderPipeline=previous;}
    }
    static Vector3[] Vertices(SkinnedMeshRenderer renderer) {
        var mesh=new Mesh();renderer.BakeMesh(mesh,true);
        var result=mesh.vertices.Select(v=>renderer.transform.TransformPoint(v)).ToArray();
        UnityEngine.Object.DestroyImmediate(mesh);return result;
    }
    static float Difference(Vector3[] a,Vector3[] b)=>a.Select((v,i)=>Vector3.Distance(v,b[i])).Max();
}
