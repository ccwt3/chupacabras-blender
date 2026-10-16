using UnityEngine;

namespace Chupacabras {
    // Tracking disables the hierarchy; restart before rendering the recovered scene.
    [RequireComponent(typeof(Animator))]
    public sealed class AttackPlayback : MonoBehaviour {
        bool restart;
        public void RestartSequence() { restart = true; }
        void OnDisable() { RestartSequence(); }
        void Update() {
            if (!restart) return;
            var animator = GetComponent<Animator>();
            animator.Play("Ataque", 0, 0);
            animator.Update(0);
            restart = false;
        }
    }
}
