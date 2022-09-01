import os
import glob
import hashlib
import subprocess 
import contextlib

@contextlib.contextmanager
def chdir(target):
    try:
        start = os.getcwd()
        os.chdir(target)
        yield

    finally:
        os.chdir(start)


def filter_names(folder='posts', ext=".docx"):
    # return [fname  for fname in os.getenv('QUARTO_PROJECT_INPUT_FILES') if fname.endswith(ext)]
    return glob.glob(f"{folder}/**/*{ext}", recursive=True)


def checksum(fname):
    return hashlib.md5(open(fname,'rb').read()).hexdigest()


def docx2qmd():
    curdir = os.getcwd()
    converted_qmd = []
    for fname in filter_names():
        dirname = os.path.dirname(os.path.abspath(fname))
        with chdir(dirname):
            standalone_fname = os.path.basename(fname)
            chksum_fname = checksum(standalone_fname)
            chksum_frontmatter = checksum("frontmatter.txt")
            chksum = chksum_fname+chksum_frontmatter
            if os.path.exists('.checksum'):
                with open(".checksum", 'r') as old_chksum_fname: 
                    if chksum == old_chksum_fname.read(): continue
 
            cmd = f"quarto pandoc --from docx --to gfm --output generated.md --columns 9999 --extract-media=. --standalone {standalone_fname}"
            out = subprocess.check_output(cmd, shell=True)
            os.unlink("index.qmd")
            with open("index.qmd", "ab") as index_qmd, open("frontmatter.txt", "rb") as frontmatter, open("generated.md", "rb") as generated_md, open('.checksum', 'w') as chksum_out:
                index_qmd.write(frontmatter.read())
                index_qmd.write(b"\n")
                index_qmd.write(generated_md.read())
                chksum_fname = checksum(standalone_fname)
                chksum_frontmatter = checksum("frontmatter.txt")
                chksum = chksum_fname+chksum_frontmatter
                chksum_out.write(chksum)

            
            os.unlink("generated.md")
            converted_qmd.append(os.path.relpath(os.path.abspath("index.qmd"), curdir))
    return converted_qmd



def org2qmd():
    pass

def convert():
    # print(os.getenv('QUARTO_PROJECT_RENDER_ALL'))
    # print(os.getenv('QUARTO_PROJECT_OUTPUT_DIR'))
    print(os.getenv('QUARTO_PROJECT_INPUT_FILES'))
    # print(os.getenv('QUARTO_PROJECT_OUTPUT_FILES'))
    # print(list(filter_names()))
    docqmds = docx2qmd()
    print(docqmds)
    input_files = os.getenv('QUARTO_PROJECT_INPUT_FILES')+"\n"+"\n".join(docqmds)
    print(input_files)
    os.environ['QUARTO_PROJECT_INPUT_FILES'] = input_files


if __name__=='__main__':
    convert()