# bash ./scripts/eval_2_player.sh --step --games  --include_other_models --include_rules_based --best_moves --env

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
                    docker exec -it selfplay python3 test.py -g $2 -w $BEST -e $6 -a "$(basename -- $f .zip)" "$(basename -- $g .zip)"
                    let "counter2=0" 
                fi
                let "counter2+=1" 
            fi
        done

        let "counter1=0" 
        
        if [ $4 == 1 ]
        then
            echo "Processing $f rules based agent..."
            docker exec -it selfplay python3 test.py -g $2 -w $BEST -e $6 -a "$(basename -- $f .zip)" rules
        fi

    fi


    let "counter1+=1" 
done


counter2=$1

if [ $4 == 1 ]
then
    for g in ${FILES[@]}
    do
        if [ $counter2 == $1 ]
        then
            echo "Processing rules based $g..."
            docker exec -it selfplay python3 test.py -g $2 -w $BEST -e $6 -a rules "$(basename -- $g .zip)"
            let "counter2=0" 
        fi
        let "counter2+=1" 
        
    done

    echo "Processing rules based vs rules based ..."
    docker exec -it selfplay python3 test.py -g $2 -w $BEST -e $6 -a rules rules

fi

