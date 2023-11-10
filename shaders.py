vertex_shader = '''
#version 450 core
layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

out vec2 UVs;

void main()
{
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(position, 1.0);
    UVs = texCoords;
}
'''

fragment_shader = '''
#version 450 core

layout (binding = 0) uniform sampler2D tex;

in vec2 UVs;

out vec4 fragColor;

void main()
{
    
    fragColor = texture(tex, UVs);
}
'''

colors_shader = '''
#version 450 core

uniform float time; 

in vec2 UVs;

out vec4 fragColor;

void main()
{
    float red = abs(sin(time)); 
    float green = abs(sin(time + 2.0944)); 
    float blue = abs(sin(time + 4.18879)); 

    fragColor = vec4(red, green, blue, 1.0);
}
'''

plasma_shaders = ''' 
#version 450 core

uniform float time;
out vec4 fragColor;

void main()
{
    vec2 uv = gl_FragCoord.xy / vec2(960.0, 540.0); 
    uv -= 0.5; 
    uv *= 2.0;

    float wave1 = sin(uv.x * 10.0 + time) * 0.5 + 0.5;
    float wave2 = cos(uv.y * 10.0 - time) * 0.5 + 0.5;

    float plasma = wave1 * wave2;

    vec3 color = vec3(plasma, plasma * 0.5, sin(time + plasma * 2.0));

    fragColor = vec4(color, 1.0);
}
'''

breathe_shader = '''
#version 450 core
layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;
uniform float time;

out vec2 UVs;

void main()
{
    vec3 pos = position;
    
    
    float infladoFactor = sin(time *2.0 + length(pos) * 4.0) * 0.1;

    vec3 normal = vec3(0.0, 0.0, 1.0);
    pos += normal * infladoFactor;

    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(pos, 1.0);
    UVs = texCoords;
}
'''

barca_shader = '''
#version 450 core

uniform float time;
in vec2 UVs;
in vec3 transformedPosition; 

out vec4 fragColor;

void main()
{
    float mixFactor = sin(time * 8.0);

    float positionFactor = sign(transformedPosition.x);

    vec4 colorA = vec4(1.0, 0.0, 0.0, 1.0); 
    vec4 colorB = vec4(0.0, 0.0, 1.0, 1.0); 

    vec4 mixedColor = mix(colorA, colorB, (positionFactor * mixFactor + 1.0) / 2.0);

    fragColor = mixedColor;
}
'''

barca_vertex_shader = ''' 
#version 450 core
layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

out vec2 UVs;
out vec3 transformedPosition;

void main()
{
    vec4 worldPosition = modelMatrix * vec4(position, 1.0);
    transformedPosition = worldPosition.xyz;
    gl_Position = projectionMatrix * viewMatrix * worldPosition;
    UVs = texCoords;
}
'''