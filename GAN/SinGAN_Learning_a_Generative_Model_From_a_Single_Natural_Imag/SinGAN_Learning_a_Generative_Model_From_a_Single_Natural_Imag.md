1. unconditional GAN

   unconditional GANs have shown remarkable success in generating realistic, high quality samples when trained on class speciﬁc datasets (e.g., faces [33], bedrooms[47]).

   Unconditional single image GANs have been explored only in the context of texture generation[3, 27, 31].

2. Modeling the internal distribution of patches within a single natural image

   Modeling the internal distribution of patches within a single natural image has been long recognized as a powerful prior in many computer vision tasks.

3. At the coarsest scale, the generation is purely generative, i.e. G <sub>N</sub> maps [**spatial white Gaussian noise**](https://baike.baidu.com/item/%E9%AB%98%E6%96%AF%E7%99%BD%E5%99%AA%E5%A3%B0/3547261#3) z<sub> N</sub> to an image sample $\tilde{x} $<sub> N</sub> .

4. Note that our goal is not image retargeting – our image samples are random and optimized to maintain the patch statistics, rather than preserving salient objects. See SM for more results and qualitative comparison to image retargeting methods.

5. To quantify the diversity of the generated images, for each training example we calculated the standard deviation (std) of the intensity values of each pixel over 100 generated images, averaged it over all pixels, and normalized by the std of the intensity values of the training image.

6. [图像金字塔](https://blog.csdn.net/Eastmount/article/details/89341077/)

