#version 400 core

out vec4 FragColor;

in vec2 TexCoord;

uniform sampler2D tex;
uniform bool useDepth;

float near = 0.1; 
float far  = 10.0; 
  
float LinearizeDepth(float depth) 
{
    float z = depth * 2.0 - 1.0; // back to NDC 
    return (2.0 * near * far) / (far + near - z * (far - near));	
}

void main() {
	if (useDepth)
	{
		float depth = LinearizeDepth(gl_FragCoord.z) / far; // divide by far for demonstration
		FragColor = vec4(vec3(depth), 1.0);
	}
	else
		FragColor = texture(tex, TexCoord).rgba;
	
}