vertex_shader = """
# version 330

layout(location = 0) in vec3 a_position;
layout(location = 1) in vec2 a_texture;
layout(location = 2) in vec3 a_normal;

uniform mat4 model;
uniform mat4 projection;
uniform mat4 view;

out vec2 v_texture;

void main()
{
    gl_Position = projection * view * model * vec4(a_position, 1.0);
    v_texture = a_texture;
}
"""

fragment_shader = """

# version 330

in vec2 v_texture;
in vec3 fragNormal;

out vec4 out_color;

uniform sampler2D s_texture;

void main()
{
    vec3 ambientLightIntensity = vec3(0.3f, 0.2f, 0.4f);
    vec3 sunlightIntensity = vec3(0.9f, 0.9f, 0.9f);
    vec3 sunlightDirection = normalize(vec3(4.0f, 4.0f, -2.0f));

    vec4 texel = texture(s_texture, v_texture);

    vec3 lightIntensity = ambientLightIntensity + sunlightIntensity + max(dot(fragNormal, sunlightDirection), 0.0f);

    //out_color = texture(s_texture, v_texture);
    out_color = vec4(texel.rgb * lightIntensity, texel.a);
}
"""