if [ "$#" -ne 1 ]; then
    echo "Usage: ./run.sh <url>"
    exit 1
fi

clear
python3 main.py $1