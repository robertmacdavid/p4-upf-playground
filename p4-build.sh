ME=`basename $0`
if [ $# -eq 0 ]
  then
    echo "Usage: $ME <program.p4>"
    exit 1
fi


P4C_IMG=p4lang/p4c:latest

P4FILE=$1
P4CARGS=${2-""}
FILENAME=`basename "${P4FILE}"`
FILEPATH="$(cd "$(dirname "${P4FILE}")"; pwd -P)"

BUILDDIR="p4build"
rm -rf p4build

echo "Building P4 program. Output will be in ${BUILDDIR}"
mkdir -p $FILEPATH/${BUILDDIR}
docker run --rm -v ${FILEPATH}:/workdir -w /workdir ${P4C_IMG} \
		p4c-bm2-ss --arch v1model -o ${BUILDDIR}/bmv2.json \
            --p4runtime-files ${BUILDDIR}/p4info.txt --Wdisable=unsupported \
        ${P4CARGS} \
		${FILENAME}
mv $FILEPATH/$BUILDDIR $BUILDDIR
echo "Done."
