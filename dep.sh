export TARGET=../dist
export BACKUP=../backup
#backup img
cp -rR $TARGET/dbimg $BACKUP/

cd front 
npm run build 

echo "cd .."
cd ..
mkdir $TARGET
mkdir $BACKUP
echo "copy *.py"
cp app.py $TARGET/.

mkdir $TARGET/front
mkdir $TARGET/back
#take car to never remove
mkdir $TARGET/dbimg
mkdir $BACKUP/dbimg
#restore img
cp -rR $BACKUP/dbimg $TARGET/.
cp front/src/assets/img/avatar/default_avatar.png $TARGET/dbimg/.

cp front/*.py $TARGET/front/.
cp -rR back $TARGET/.

echo launch python
python ../dist/app.py
