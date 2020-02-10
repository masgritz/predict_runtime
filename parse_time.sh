#!/bin/bash
#/home/masgritz/benchmark/output_beholder4/bt/A/1
DIR='/home/masgritz/benchmark/nas_abc_output/output_new'
APP=('bt' 'cg' 'dc' 'ep' 'ft' 'is' 'lu' 'mg' 'sp' 'ua')
SIZE=('S' 'W' 'A' 'B' 'C') #'16384')
THREAD=('1' '2' '4' '6' '8' '10' '12')
FILENAME='output'
FULLNAME=''

for((g=0; g < ${#APP[@]}; g++)); do

	for((h=0; h < ${#SIZE[@]}; h++)); do

		for((i=0; i < ${#THREAD[@]}; i++)); do
			mkdir -p $DIR/new/

			for ((j=0; j<30; j++)) ; do
				#echo ${FILENAME}'_'${APP[g]}'_'${THREAD[i]}'_'${SIZE[h]}'_'${j}'.dat'
				head -n 23 $DIR/${FILENAME}'_'${APP[g]}'_'${SIZE[h]}'_'${THREAD[i]}'_'${j}'.dat' > $DIR/new/${FILENAME}'_'${APP[g]}'_'${SIZE[h]}'_'${THREAD[i]}'_'${j}'_new.dat'
				echo "${APP[g]}|App||" >> $DIR/new/${FILENAME}'_'${APP[g]}'_'${SIZE[h]}'_'${THREAD[i]}'_'${j}'_new.dat'
				echo "${SIZE[h]}|Size||" >> $DIR/new/${FILENAME}'_'${APP[g]}'_'${SIZE[h]}'_'${THREAD[i]}'_'${j}'_new.dat'
				echo "${THREAD[i]}|Thread||" >> $DIR/new/${FILENAME}'_'${APP[g]}'_'${SIZE[h]}'_'${THREAD[i]}'_'${j}'_new.dat'
				echo "${j}|Run||" >> $DIR/new/${FILENAME}'_'${APP[g]}'_'${SIZE[h]}'_'${THREAD[i]}'_'${j}'_new.dat'
				cat $DIR/${FILENAME}'_'${APP[g]}'_'${SIZE[h]}'_'${THREAD[i]}'_'${j}'.dat' | grep system | awk '{ print $3 }' >> $DIR/new/${FILENAME}'_'${APP[g]}'_'${SIZE[h]}'_'${THREAD[i]}'_'${j}'_new.dat'
				#mv $DIR/new/${FILENAME}'_'${APP[g]}'_'${SIZE[h]}'_'${THREAD[i]}'_'${j}'_new.dat' $DIR/${FILENAME}'_'${APP[g]}'_'${SIZE[h]}'_'${THREAD[i]}'_'${j}'.dat'
			done ;

			#rm -r $DIR/${APP[g]}/${SIZE[h]}/${THREAD[i]}/new/

		done ;
	done ;
done ;
