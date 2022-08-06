#version 460

in vec3 out_normal;
in vec2 out_uv;

uniform sampler2D tex;

out vec4 fragColor;

void main()
{
    fragColor = vec4(out_normal, 1.) * texture(tex, out_uv); 
}