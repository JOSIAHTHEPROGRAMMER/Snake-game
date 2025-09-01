# Snake Game (Pygame)

A classic Snake game built with **Python** and **Pygame**, featuring a grid, score tracking, pause functionality, and wrap-around movement.  
The snake grows as it eats apples, and the game ends when the snake collides with itself.  

---

## Features
- Responsive **resizable window**
- **Grid-based gameplay** with block size of 60px
- **Custom graphics** for snake head, body, and apples
- **Screen wrapping** (snake reappears on the opposite side)
- **Pause/Unpause** with `P` key
- **Game Over screen** with restart option (`R`)
- Score display at the top
- Custom **Minecraft font** for UI

---

## Controls
| Key | Action |
|-----|--------|
| ⬆️ / ⬇️ / ⬅️ / ➡️ | Move snake (no 180° turns allowed) |
| **P** | Pause / Unpause game |
| **R** | Restart after Game Over |
| **Esc / Window close** | Quit game |

---

## Assets
Make sure the following files are in the same folder as the script:
- `snake_head.png` → Snake head image  
- `snake_body.png` → Snake body segment  
- `apple.png` → Apple image  
- `Minecraft.ttf` → Font file for text  

---

##  Installation & Run
1. Clone or download this project.
2. Install [Python 3.8+](https://www.python.org/downloads/).
3. Install **Pygame**:
   ```bash
   pip install pygame
   ```
4. Run in IDE of choice
