workdir=$(pwd)

git pull && git push
hugo --minify && cp -r public/* ../thiscute.world-gh-pages

cd ../thiscute.world-gh-pages
git add .
git commit -am "feat: update posts"
git push
cd $workdir
