#ssh -vT git@github.com
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/git_rsa
