
run()
{
    nohup uvicorn main:app --host 0.0.0.0 --port 5000 &
    echo "run"
}

kill()
{
    sudo killall uvicorn
    echo "kill"
}

echo "usage: source server.sh; [run|kill]"