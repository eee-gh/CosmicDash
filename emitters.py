import random
import arcade

from arcade.particles import FadeParticle, Emitter, EmitBurst, EmitInterval, EmitMaintainCount

SPARK_TEX = [
    arcade.make_soft_circle_texture(8, arcade.color.PASTEL_YELLOW),
    arcade.make_soft_circle_texture(8, arcade.color.PEACH),
    arcade.make_soft_circle_texture(8, arcade.color.BABY_BLUE),
    arcade.make_soft_circle_texture(8, arcade.color.ELECTRIC_CRIMSON),
]
SMOKE_TEX = arcade.make_soft_circle_texture(20, arcade.color.LIGHT_GRAY, 255, 80)
PUFF_TEX = arcade.make_soft_circle_texture(12, arcade.color.WHITE, 255, 50)


def make_trail(attached_sprite, maintain=60):
    emit = Emitter(
        center_xy=(attached_sprite.center_x, attached_sprite.center_y),
        emit_controller=EmitMaintainCount(maintain),
        particle_factory=lambda e: FadeParticle(
            filename_or_texture=random.choice(SPARK_TEX),
            change_xy=arcade.math.rand_in_circle((0.0, 0.0), 1.6),
            lifetime=random.uniform(0.35, 0.6),
            start_alpha=220, end_alpha=0,
            scale=random.uniform(0.25, 0.4),
        ),
    )

    emit._attached = attached_sprite
    return emit
