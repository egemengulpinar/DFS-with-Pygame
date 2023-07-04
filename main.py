import pygame
import time
import asyncio

class Solution:
    def __init__(self):
        self.res = 0
        self.grid_history = []
        self.solution_path = []

    def uniquePathsIII(self, grid):
        m, n, empty = len(grid), len(grid[0]), 1
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1:
                    x, y = (i, j)
                elif grid[i][j] == 2:
                    end = (i, j)
                elif grid[i][j] == 0:
                    empty += 1
        self.dfs(grid, x, y, end, empty)
        if self.res == 0:
            self.animate_solution(blank=True)
        return self.res

    def dfs(self, grid, x, y, end, empty):
        if not (0 <= x < len(grid)) or not (0 <= y < len(grid[0])) or grid[x][y] < 0:
            return 
        if (x, y) == end:
            if empty == 0:
                self.res += 1
                self.solution_path = [row[:] for row in grid]
                response = self.animate_solution(blank=False)
            return 

        # Save the current state of the grid for animation
        self.grid_history.append([row[:] for row in grid])

        grid[x][y] = -2
        self.dfs(grid, x + 1, y, end, empty - 1)
        self.dfs(grid, x - 1, y, end, empty - 1)
        self.dfs(grid, x, y + 1, end, empty - 1)
        self.dfs(grid, x, y - 1, end, empty - 1)
        grid[x][y] = 0
        

    def animate_solution(self,blank):
        # Define constants
        TILE_SIZE = 40
        TILE_MARGIN = 5
        TILES_X = len(self.grid_history[0][0])
        TILES_Y = len(self.grid_history[0])
        LEGEND_WIDTH = 200
        WINDOW_WIDTH = TILES_X * (TILE_SIZE + TILE_MARGIN) + LEGEND_WIDTH
        WINDOW_HEIGHT = TILES_Y * (TILE_SIZE + TILE_MARGIN)

        # Define colors
        COLORS = {
            1: (0, 255, 0),  # Green for the start tile
            0: (255, 255, 255),  # White for empty tiles
            2: (255, 0, 0),  # Red for the end tile
            -1: (0, 0, 0),  # Black for blocked tiles
            -2: (0, 0, 255)  # Blue for visited tiles
        }

        # Color descriptions
        DESCRIPTIONS = {
            1: "Start Tile",
            0: "Empty Tiles",
            2: "End Tile",
            -1: "Blocked Tiles",
            -2: "Visited Tiles"
        }

        # Initialize pygame and the window
        pygame.init()
        window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        font = pygame.font.Font(None, 36)

        # Function to draw the grid
        def draw_grid(grid):
            for y, row in enumerate(grid):
                for x, tile in enumerate(row):
                    rect = pygame.Rect(x*(TILE_SIZE+TILE_MARGIN), y*(TILE_SIZE+TILE_MARGIN), TILE_SIZE, TILE_SIZE)
                    pygame.draw.rect(window, COLORS[tile], rect)

        # Function to draw the legend
        def draw_legend():
            for i, color in enumerate(COLORS):
                rect = pygame.Rect(WINDOW_WIDTH - LEGEND_WIDTH + 10, i*(TILE_SIZE+TILE_MARGIN) + 10, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(window, COLORS[color], rect)

                text = font.render(DESCRIPTIONS[color], True, (255, 255, 255))
                window.blit(text, (WINDOW_WIDTH - LEGEND_WIDTH + 10 + TILE_SIZE + 10, i*(TILE_SIZE+TILE_MARGIN) + 10))

        # Function to update the window
        def update_window(grid):
            window.fill((0, 0, 0))  # Fill the window with black
            draw_grid(grid)  # Draw the grid
            draw_legend()  # Draw the legend
            pygame.display.flip()  # Update the display
        if blank:
            text = font.render("PATH NOT FOUND : {}".format(self.res), True, (255, 0, 0))
            window.blit(text, (WINDOW_WIDTH / 2 - text.get_width() / 2, WINDOW_HEIGHT / 2 - text.get_height() / 2))
            pygame.display.flip()
            time.sleep(5)
            return False
                # Display "FOUND" message and show the solution path
        text = font.render("FOUND : {}".format(self.res), True, (255, 0, 0))
        window.blit(text, (WINDOW_WIDTH / 2 - text.get_width() / 2, WINDOW_HEIGHT / 2 - text.get_height() / 2))
        pygame.display.flip()
        time.sleep(2)
        for grid_state in self.grid_history[-10::1]:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Quit the game
                    return
            update_window(grid_state)  # Update the window
            time.sleep(0.5)  # Delay to make the animation visible
        return True

async def main():
    s = Solution()
    grid = [[1,0,0,0],[0,0,0,0],[2,0,0,-1]]
    s.uniquePathsIII(grid)
    await asyncio.sleep(0)
if __name__ == "__main__":
    asyncio.run(main())

