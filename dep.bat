set TARGET=C:\Users\berny\dev\dep

cp app.py %TARGET%/.

mkdir %TARGET%/css
mkdir %TARGET%/img
mkdir %TARGET%/js
mkdir %TARGET%/front
mkdir %TARGET%/back

cp front/dist/* %TARGET%/.
cp front/dist/css/* %TARGET%/css/.
cp front/dist/img/* %TARGET%/img/.
cp front/dist/js/* %TARGET%/js/.

cp front/*.py %TARGET%/front/.

cp -rR back/* %TARGET%/back/.