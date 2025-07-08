import os
import shutil

template_file = "plumed.dat"
tpr_file = "ala2.tpr"

with open(template_file, "r") as f:
    template = f.read()

for i in range(1, 21):
    folder = str(i)
    os.makedirs(folder, exist_ok=True)

    shutil.copy(tpr_file, folder)

    replaced = template.replace(
        "../../../train/SelfTICA_NN/1/model.ptc",
        f"../../../train/SelfTICA_NN/{i}/model.ptc"
    )
    with open(os.path.join(folder, "plumed.dat"), "w") as out:
        out.write(replaced)

