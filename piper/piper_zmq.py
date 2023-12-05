import subprocess
import zmq
import sys
sys.path.append('../')
from common.pubsub import Pubsub

ps = Pubsub(name="piper")


def say(phrase):
# Define the first part of the pipe
    subprocess.run(['killall', 'aplay'])
    subprocess.run(['killall', 'piper'])

    p1 = subprocess.Popen(['echo', phrase], stdout=subprocess.PIPE)


#    modelname = "en_US-lessac-medium"
    modelname = "en_GB-alan-medium"

# Define the second part of the pipe
    p2 = subprocess.Popen(["./piper/piper", "--model", "piper/voices/" + modelname + ".onnx", "--output-raw"], stdin=p1.stdout, stdout=subprocess.PIPE)

    p3 = subprocess.Popen("aplay -r 22050 -f S16_LE -t raw -".split(" "), stdin=p2.stdout, stdout=subprocess.PIPE)


# Close the first process's output to allow p1 to receive a SIGPIPE if p2 exits
    p1.stdout.close()
    p2.stdout.close()

# Get the output
    output = p3.communicate()[0]
    print(output.decode())


while True:
    message = ps.recv_string()
    print(message)

    if("::say:::" in message):
        phrase = message.split("::say:::")[1]
        print(phrase)
        say(phrase)
        print("just said phrase", phrase)

 
#echo 'Hello! How are you?' | ./piper --model voices/en_GB-alan-medium.onnx --output-raw | aplay -r 22050 -f S16_LE -t raw -
