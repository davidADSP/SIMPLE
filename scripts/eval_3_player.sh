# bash ./scripts/eval.sh $1 (step) $2 (games) $3 (include_other_models) $4 (include_rules_based) $5 (best_moves) $6 (env)

if [ $5 == 1 ]
then
BEST='-b'
else
BEST=''
fi

rm ./app/viz/results.csv
declare -a FILES=("./app/zoo/$6/best_model.zip")


FILES+=(./app/zoo/$6/_model*.zip)

echo "${FILES[@]}"

counter1=$1
counter2=$1
for f in ${FILES[@]}
do
    let "counter2=$1" 
    if [ $counter1 == $1 ]
    then
        for g in ${FILES[@]}
        do
            if [ $3 == 1 ]
            then
                if [ $counter2 == $1 ]
                then
                    echo "Processing $f $g..."
                    docker exec -it selfplay python3 test.py -g $2 -w $BEST -e $6 -a "$(basename -- $f .zip)" "$(basename -- $g .zip)" "$(basename -- $g .zip)"
                    let "counter2=0" 
                fi
                let "counter2+=1" 
            fi
        done

        let "counter1=0" 


    fi


    let "counter1+=1" 
done

