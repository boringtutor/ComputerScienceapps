from Board import Board 
from pynput import keyboard
from time import sleep

b = Board()

def main():
    b.shuffle()
    b.refresh()

def on_press(key):
    b.refresh()
    
def on_release(key):
    
    if key == keyboard.Key.esc:
        # Stop listener
        return False
    elif key == keyboard.Key.up:
       b.board , b.e_loc = b.moveup(b.board,b.e_loc)
    elif key == keyboard.Key.right:
       b.board , b.e_loc = b.moveright(b.board,b.e_loc)
    elif key == keyboard.Key.left:
       b.board , b.e_loc = b.moveleft(b.board,b.e_loc)
    elif key == keyboard.Key.down:
       b.board , b.e_loc = b.movedown(b.board,b.e_loc)
    elif key == keyboard.Key.space:
        print('The AI is Thinking .... ')
        moves = b.solve()
        for m in moves :
            b.moves[m](b.board,b.e_loc)
            b.refresh()
            sleep(1)
    
    return b.refresh()

if __name__ == "__main__":
    main()
    # Collect events until released
    with keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()