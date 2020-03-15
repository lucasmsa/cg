vertex_shader = """
# version 330

layout(location = 0) in vec3 a_position;
layout(location = 1) in vec2 a_texture;

uniform mat4 model; // combined rotation and translation
uniform mat4 projection;
uniform mat4 view;

out vec3 v_color;
out vec2 v_texture;

void main()
{
    
    gl_Position = projection * view * model * vec4(a_position, 1.0);//  read it right to left. Multiplying each space
    v_texture = a_texture;
}
"""

fragment_shader = """
# version 330
in vec2 v_texture;
out vec4 out_color;
uniform sampler2D s_texture;
void main()
{
    out_color = texture(s_texture, v_texture);
}
"""