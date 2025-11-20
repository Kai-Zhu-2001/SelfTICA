import os
import shutil

template_file = "plumed.dat"
input_file = "md_input"
potential_file = 'md_potential'

with open(template_file, "r") as f:
    template = f.read()

for i in range(0, 25):
    folder = str(i)
    os.makedirs(folder, exist_ok=True)

    shutil.copy(input_file, folder)
    shutil.copy(potential_file, folder)

    replaced = template.replace(
        "../../../models/DeepTICA/model_0.ptc",
        f"../../../models/DeepTICA/model_{i}.ptc"
    )
    with open(os.path.join(folder, "plumed.dat"), "w") as out:
        out.write(replaced)
