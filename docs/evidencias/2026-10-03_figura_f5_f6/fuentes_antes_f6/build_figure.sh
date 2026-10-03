#!/usr/bin/env bash
set -euo pipefail
PROJECT_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
UNITY_EDITOR='/home/cacawatin/Unity/Hub/Editor/6000.3.22f1/Editor/Unity'
cd "$PROJECT_ROOT"
export CHUPA_FIGURE_STAGE="${CHUPA_FIGURE_STAGE:-F1}"
case "$CHUPA_FIGURE_STAGE" in F1|F4) ;; *) echo 'Expected F1 or F4' >&2; exit 2 ;; esac
export CHUPA_FIGURE_EVIDENCE="${CHUPA_FIGURE_EVIDENCE:-docs/evidencias/${CHUPA_FIGURE_STAGE}_$(date -u +%Y%m%d_%H%M%S)}"
mkdir "$CHUPA_FIGURE_EVIDENCE"
export DOTNET_PROCESSOR_COUNT=2
export GRADLE_USER_HOME="$PROJECT_ROOT/Library/GradleUserHome"
FIGURE_REV=r01
if [[ "$CHUPA_FIGURE_STAGE" == F4 ]]; then FIGURE_REV=r02; fi
if [[ ! -f Assets/Scenes/${CHUPA_FIGURE_STAGE}_FiguraAR_${FIGURE_REV}.unity ]]; then
  "$UNITY_EDITOR" -job-worker-count 2 -batchmode -quit -projectPath "$PROJECT_ROOT" \
    -executeMethod FigureBuild.Configure -logFile "$CHUPA_FIGURE_EVIDENCE/configure.log"
fi
"$UNITY_EDITOR" -job-worker-count 2 -batchmode -quit -projectPath "$PROJECT_ROOT" \
  -executeMethod FigureBuild.Verify -logFile "$CHUPA_FIGURE_EVIDENCE/verify.log"
"$UNITY_EDITOR" -job-worker-count 2 -batchmode -projectPath "$PROJECT_ROOT" \
  -executeMethod FigurePreview.Capture -logFile "$CHUPA_FIGURE_EVIDENCE/runtime.log"
"$UNITY_EDITOR" -job-worker-count 2 -batchmode -nographics -quit -projectPath "$PROJECT_ROOT" -buildTarget Android \
  -executeMethod FigureBuild.BuildAndroid -logFile "$CHUPA_FIGURE_EVIDENCE/build.log"
python scripts/verify_figure_apk.py "$CHUPA_FIGURE_EVIDENCE"
