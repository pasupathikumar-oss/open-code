uniform sampler2D bgl_RenderedTexture;

void main()
{
    vec4 sum = vec4(0);
    vec2 texcoord = vec2(gl_TexCoord[0]).st;
    int j;
    int i;

    for( i= -1 ;i < 1; i++)
    {
        for (j = -1; j < 1; j++)
        {
    sum += texture2D(bgl_RenderedTexture, texcoord + (vec2(i, j)*.001))*.3; 
}}

    //gl_FragColor = sum;
    gl_FragColor = (sum*sum)+(texture2D(bgl_RenderedTexture, texcoord));
}