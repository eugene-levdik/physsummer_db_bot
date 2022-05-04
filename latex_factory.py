def build_pdf(problems, filename, teachermode=True, tagsmode=True, setphysstyle=None, printtask=False):
    tex_file = open(f'{filename}.tex', 'w')
    tex_file.write('''\\documentclass[a4paper, 12pt]{article}

\\usepackage{amssymb}
\\usepackage{amsmath}
\\usepackage{mathrsfs}
\\usepackage{"physsummer_style/physsummer"}

\\usepackage[margin=1.5cm,
    		marginparsep=0.2cm,
    		headsep=0.5cm,
    		footskip=1cm,
    		marginparwidth=1cm]{geometry}

\\tolerance = 1000
\\emergencystretch = 0.74cm

\\pagestyle{empty}
\\parindent = 0mm


\\begin{document}

''')
    if setphysstyle is not None:
        arg1, arg2, arg3 = setphysstyle
        tex_file.write(f'\\setphysstyle{{{arg1}}}{{{arg2}}}{{{arg3}}} \n')
    if teachermode:
        tex_file.write('\\teachermode \n')
    if tagsmode:
        tex_file.write('\\tagsmode \n')
    if printtask:
        tex_file.write('\\printtrue \n\n\\printtask{\n')

    for problem in problems:
        book_name, problem_name = problem
        tex_file.write('\t\\libproblem{' + book_name + '}{' + problem_name + '} \n')

    if printtask:
        tex_file.write('}\n')

    tex_file.write('\n\\end{document} \n')
    tex_file.close()

    bashCommand = f"pdflatex -interaction=nonstopmode {filename}.tex"
    import subprocess
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    pdf_file = open(f'{filename}.pdf', 'rb')
    tex_file = open(f'{filename}.tex', 'rb')

    return pdf_file, tex_file
