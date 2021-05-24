export TARGET=../dist
cd front 
npm run build 

echo "cd .."
cd ..

echo "copy *.py"
cp app.py $TARGET/.

mkdir $TARGET/front
mkdir $TARGET/back

cp front/*.py $TARGET/front/.
cp -rR back $TARGET/.