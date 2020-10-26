We introduced **multiple discriminators** into the GAN framework 

and explored **discriminator** roles ranging **from a formidable adversary to a forgiving teacher**. 

Allowing the generator to **automatically tune its learning schedule** outperformed GANs with a single discriminator on MNIST. 

In general, GMAN variants achieved faster convergence to a higher quality steady state on a variety of tasks as measured by a **GAM-type metric (GMAM)**. 

In addition,  GMAN makes using the original GAN objective possible **by increasing the odds of the generator** receiving constructive feedback.



读完，只能说很ICLR，和其他计算机视觉顶会一样，并不注重并行和分布式，并不注重训练的加速。

