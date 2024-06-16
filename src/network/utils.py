def decode(message : str) -> tuple[int,int] | None:
    spl = message.split(",")
    try:
        return int(spl[0]), int(spl[1])
    except:
        return None
        
def encode(x : int, y : int):
    return str(x) + "," + str(y)