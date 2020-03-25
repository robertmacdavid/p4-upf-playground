ME=`basename $0`
if [ $# -ne 1 ]
  then
    echo "Usage: $ME <program.p4>"
    exit 1
fi


P4C_IMG=p4lang/p4c:latest

P4FILE=$1
FILENAME=`basename "${P4FILE}"`
FILEPATH="$(cd "$(dirname "${P4FILE}")"; pwd -P)"

BUILDDIR="p4build"

echo "Building P4 program. Output will be in ${FILEPATH}/${BUILDDIR}"
mkdir -p $FILEPATH/${BUILDDIR}
docker run --rm -v ${FILEPATH}:/workdir -w /workdir ${P4C_IMG} \
		p4c-bm2-ss --arch v1model -o ${BUILDDIR}/bmv2.json \
            --p4runtime-files ${BUILDDIR}/p4info.txt --Wdisable=unsupported \
		${FILENAME}
echo "Done."
