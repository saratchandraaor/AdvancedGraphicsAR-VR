#version 460

in vec3 in_vertex;
in vec3 in_normal;
in vec2 in_uv;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

out vec3 out_normal;
out vec2 out_uv;

void main()
{
    // gl_Position has to be set
    gl_Position = projection * view * model * vec4(in_vertex, 1.);
    out_normal = in_normal;
    out_uv = in_uv;
}