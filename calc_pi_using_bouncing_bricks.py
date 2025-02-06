# Basic framework for a Python script to animate
# calculating Pi using Bouncing objects.
# Dave Parsons.
# Jan 2025
#
#

import sys
import pygame
import pymunk
import pymunk.pygame_util

COLL_TYPE_BIG=3
COLL_TYPE_SMALL=4

collision_count=0

def collision_begin(arbiter, space, data):
    global collision_count
    collision_count += 1
    return True

def add_vertical_barrier(space,x,y,h):
    # Create a static body for the barrier
    body = pymunk.Body(body_type=pymunk.Body.STATIC)

    # Define the shape of the barrier (e.g., a line segment)
    segment_shape = pymunk.Segment(body, (x, y-h), (x, y+h), 20)  # (x1, y1), (x2, y2), thickness

    segment_shape.friction = 0
    segment_shape.elasticity = 1
    segment_shape.collision_type=COLL_TYPE_BIG

    # Add the shape to the space
    space.add(body, segment_shape)


def add_cube(space, size, x,y, v=(0,0), mass=3, CollisionType=0):
    """Add a cube to the given space."""

    points = [(-size, -size), (-size, size), (size, size), (size, -size)]
    moment = pymunk.moment_for_poly(mass, points, (0, 0))
    body = pymunk.Body(mass, moment)
    body.position = x, y
    body.velocity=v

    shape = pymunk.Poly(body, points)
    shape.friction = 0
    shape.elasticity = 1

    shape.collision_type=CollisionType

    space.add(body, shape)

    return shape

def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 200))
    pygame.display.set_caption(f"Calc pi ({collision_count/100})as the number of collisions of bouncing cubes.")
    clock = pygame.time.Clock()

    space = pymunk.Space()
    space.gravity = (0.0, 0.0)

    handler = space.add_collision_handler(COLL_TYPE_BIG, COLL_TYPE_SMALL)
    handler.begin = collision_begin


    add_vertical_barrier(space,100,100,50)
    add_cube(space,10,200,100, (0,0), 1, COLL_TYPE_SMALL)
    add_cube(space,40,300,100, (-10,0),10000, COLL_TYPE_BIG)

    draw_options = pymunk.pygame_util.DrawOptions(screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sys.exit(0)

        screen.fill((255,255,255))

        space.debug_draw(draw_options)

        space.step(1/60.0)

        pygame.display.set_caption(f"Calc pi ({collision_count / 100 })as the number of collisions of bouncing cubes.")

        pygame.display.flip()

        clock.tick(60)

if __name__ == '__main__':
    main()