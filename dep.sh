export TARGET=../dist
cd front 
npm run build 

echo "cd .."
cd ..
mkdir $TARGET
echo "copy *.py"
cp app.py $TARGET/.

mkdir $TARGET/front
mkdir $TARGET/back

cp front/*.py $TARGET/front/.
cp -rR back $TARGET/.

echo launch python
python ../dist/app.py
