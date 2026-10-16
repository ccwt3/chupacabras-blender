"""Monta evidencia F2 usando FFmpeg existente; conserva imágenes originales."""
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
revision = os.environ.get('CHUPA_F2_REV','r04')
folder = ROOT/'previews'/('F2_chupacabras_forma_'+revision)


def sheet(name, entries, columns):
    output = folder/(name+'.png')
    if output.exists():
        raise FileExistsError(output)
    args = ['ffmpeg','-hide_banner','-loglevel','error','-n','-filter_complex_threads','2']
    filters = []
    for i, (filename, label) in enumerate(entries):
        args += ['-i',str(folder/(filename+'.png'))]
        filters.append(f"[{i}:v]scale=550:425,pad=550:455:0:30:color=0x242c32,drawtext=text='{label}':x=12:y=7:fontsize=17:fontcolor=white[v{i}]")
    layout = '|'.join(f'{i%columns*550}_{i//columns*455}' for i in range(len(entries)))
    filters.append(''.join(f'[v{i}]' for i in range(len(entries)))+f'xstack=inputs={len(entries)}:layout={layout}[out]')
    subprocess.run(args+['-filter_complex',';'.join(filters),'-map','[out]','-frames:v','1','-threads','2','-update','1',str(output)],check=True)


if __name__ == '__main__':
    sheet('seis_vistas', [('forma_'+v,label) for v,label in [
        ('frente','Frente'),('perfil','Perfil'),('espalda','Espalda'),
        ('tres_cuartos','Tres cuartos'),('inferior','Vista inferior'),('rostro','Rostro')]],3)
    sheet('comparacion',[('base_tres_cuartos','Base demacrada R02'),
                         ('forma_tres_cuartos','F2 '+revision+' - forma y pose')],2)
