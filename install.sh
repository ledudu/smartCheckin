#!/bin/bash

PWD=`pwd`
TARGET="$PWD/scheck"

`touch scheck`
`chmod +x scheck`

cat > scheck <<EOF
#!/bin/bash
cd $PWD
python smartCheckin > log 2>&1
cd -
EOF

cd /usr/local/bin
sudo ln -sf $TARGET
cd -
 
