
# 微面理论  
PBR（Physically Based Rendering）让我们的渲染不再依赖[经验模型]，而是真正具有物理意义。其中的原因正是因为PBR的核心：**微面理论（Microfacet theory）**。微面理论已经是 CG 渲染以及BRDF的**中心理论**，SIGGRAPH也连续很多年有针对微面理论专门的[学习课程]。  
![PBR示例](https://goolyuyi.synology.me:8889/md/pbr/zhihu/baolong-zhang-goblin-7.jpg)
_Unreal4 引擎中，PBR渲染的地精银行Goblin，图片来自[baolong zhang](https://www.artstation.com/baolong)_

不过微面理论的推导十分麻烦，在[Real Time Rendering 4th]上描述的篇幅也很有限。初次接触很容易就被搞得一脸懵逼，但作为偏执狂的作者怎么能放过这一次疯狂挑战的机会!  
![PBR效果展示](https://goolyuyi.synology.me:8889/md/pbr/zhihu/lx156t1drup4.jpg)
_PBR 可以通过2个参数均匀的模拟材质属性的变化_

所以这一篇是：  
  
- **微面理论**介绍和证明推导  
- 理解基于PBR的**BRDF函数**  
- 推导**阴影遮挡函数<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=G_2" alt="G_2">**  
- 推导**法向面分布NDF函数**  
- PBR为什么能**真实的渲染光照**  
- 需要一些微积分和概率知识  
  
我们先例行公事，做一些符号的定义：  
  
- <img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%3A%3D" alt=":="> 强调这是一个**定义**  
- <img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cleft%5Clangle%5Cmathbf%7Ba%7D%5Ccdot%5Cmathbf%7Bb%7D%5Cright%5Crangle%20%3A%3D%5Ccos%7B%28%5Ctheta_%7Bab%7D%29%7D" alt="\left\langle\mathbf{a}\cdot\mathbf{b}\right\rangle :=\cos{(\theta_{ab})}"> ，其中<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Ctheta_%7Bab%7D" alt="\theta_{ab}">是<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cmathbf%7Ba%7D" alt="\mathbf{a}">和<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cmathbf%7Bb%7D" alt="\mathbf{b}">的夹角  
- <img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Clangle%5Cmathbf%7Ba%7D%20%5Ccdot%20%5Cmathbf%7Bb%7D%5Crangle%5E%2B%3A%3D%5Cmax%7B%280%2C%5Ccos%7B%28%5Ctheta_%7Bab%7D%29%7D%29%7D" alt="\langle\mathbf{a} \cdot \mathbf{b}\rangle^+:=\max{(0,\cos{(\theta_{ab})})}"> ，其中<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Ctheta_%7Bab%7D" alt="\theta_{ab}">是<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cmathbf%7Ba%7D" alt="\mathbf{a}">和<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cmathbf%7Bb%7D" alt="\mathbf{b}">的夹角  
  
## 定义  
![角度定义](https://goolyuyi.synology.me:8889/md/pbr/zhihu/angles.png)
_角度和向量定义_

我们在[上一篇]里学到BRDF渲染函数公式，在对于任一个渲染片元（Rendering Patch）：  

<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=L_%7Bo%7D%28%5Cmathbf%7Bv%7D%29%20%20%3D%5Cint_%7B%5Cmathbf%7Bl%7D%20%5Cin%20%5COmega%7D%20f%28%5Cmathbf%7Bl%7D%2C%20%5Cmathbf%7Bv%7D%29%20L_%7Bi%7D%28%5Cmathbf%7Bl%7D%29%5Clangle%5Cmathbf%7Bn%7D%20%5Ccdot%20%5Cmathbf%7Bl%7D%5Crangle%5E%2B%20d%20%5Cmathbf%7Bl%7D%20%20%5Ctag%7B1%7D%5C%5C" alt="L_{o}(\mathbf{v})  =\int_{\mathbf{l} \in \Omega} f(\mathbf{l}, \mathbf{v}) L_{i}(\mathbf{l})\langle\mathbf{n} \cdot \mathbf{l}\rangle^+ d \mathbf{l}  \tag{1}\\">
  
其中<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=L_%7Bo%7D" alt="L_{o}">是光线传出的辉度（radiance），<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=L_%7Bi%7D" alt="L_{i}">光线传入的辉度，<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=f" alt="f">是BRDF函数。  
对于某一个具体的入射光线（也就是说，无论是场景中的点光源，平行光源，还是聚光灯或平面灯），对入射方向<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cmathbf%7Bl%7D" alt="\mathbf{l}">进行微分：  

<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=dL_%7Bo%7D%28%5Cmathbf%7Bv%7D%29%3D%20f%28%5Cmathbf%7Bl%7D%2C%20%5Cmathbf%7Bv%7D%29%20L_%7Bi%7D%28%5Cmathbf%7Bl%7D%29%5Clangle%5Cmathbf%7Bn%7D%20%5Ccdot%20%5Cmathbf%7Bl%7D%5Crangle%5E%2B%20d%20%5Cmathbf%7Bl%7D%20%20%5Ctag%7B2%7D%5C%5C" alt="dL_{o}(\mathbf{v})= f(\mathbf{l}, \mathbf{v}) L_{i}(\mathbf{l})\langle\mathbf{n} \cdot \mathbf{l}\rangle^+ d \mathbf{l}  \tag{2}\\">
  
接下来我们分离了**漫反射<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Ctext%7Bdiffuse%7D" alt="\text{diffuse}">项**和**高光<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Ctext%7Bspecular%7D" alt="\text{specular}">项**，对于漫反射项我们把渲染材质（Material）用兰伯特表面（Lambertian Surface）近似就能得到很好的效果。**然而对于高光项，我们却无法直接通过单个菲涅尔表面（Fresnel Surface）近似**，具体原因不言而喻，因为菲涅尔表面仅能在<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cmathbf%7Bl%7D" alt="\mathbf{l}">的反射方向上传递光线。  
![希望的高光Lobe](https://goolyuyi.synology.me:8889/md/pbr/zhihu/fresnel.png)
_单个菲涅尔表面无法模拟真实的高光情况，图中红色理想菲涅尔镜面反射的光，蓝色为想要模拟出来的高光反光_

先来看看最终的高光项的BRDF：  

<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=f_%7B%5Ctext%20%7B%20spec%20%7D%7D%28%5Cmathbf%7Bl%7D%2C%20%5Cmathbf%7Bv%7D%29%3D%5Cfrac%7BF%28%5Cmathbf%7Bh%7D%2C%20%5Cmathbf%7Bl%7D%29%20G_%7B2%7D%28%5Cmathbf%7Bl%7D%2C%20%5Cmathbf%7Bv%7D%2C%20%5Cmathbf%7Bh%7D%29%20D%28%5Cmathbf%7Bh%7D%29%7D%7B4%5C%2C%7C%5Cmathbf%7Bn%7D%20%5Ccdot%20%5Cmathbf%7Bl%7D%7C%5C%2C%7C%20%5Cmathbf%7Bn%7D%20%5Ccdot%20%5Cmathbf%7Bv%7D%7C%20%7D%5Ctag%7B3%7D%5C%5C" alt="f_{\text { spec }}(\mathbf{l}, \mathbf{v})=\frac{F(\mathbf{h}, \mathbf{l}) G_{2}(\mathbf{l}, \mathbf{v}, \mathbf{h}) D(\mathbf{h})}{4\,|\mathbf{n} \cdot \mathbf{l}|\,| \mathbf{n} \cdot \mathbf{v}| }\tag{3}\\">
  
其中:  
  
- <img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=G_2" alt="G_2">是**遮挡阴影函数**（masking shadowing function）  
- <img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=D" alt="D">是**法向面分布函数**（normal distribution function），我们后面简称为NDF  
- <img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=F" alt="F">是**菲涅尔反射函数**（fresnel reﬂectance function）在[上一篇]定义过  
![lanbert面，f面，实际面示例](https://goolyuyi.synology.me:8889/md/pbr/zhihu/surface.png)
_PBR的BRDF用一个兰伯特表面和多个菲涅尔表面去模拟真实情况_

看到这里千万不要慌，保持镇定！虽然我知道你满脑子的问号：遮挡阴影函数是什么？法向面分布函数是什么？分母的那个<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=4" alt="4">是干啥？但只要记住了，我们的本质想法是**用多个微小的菲涅尔镜面去近似真实世界的材质**，这就是微面理论的核心概念，剩下的我们再一一解决！  
![显微镜图](https://goolyuyi.synology.me:8889/md/pbr/zhihu/micro.png)
_对于真实世界的物体在显微镜下观察确实是有很多微小平面组成
左图为抛光塑料表面，右图为不锈钢表面_

##  高光项  
  
### 微面化渲染片元：  
![ps微面+角度定义](https://goolyuyi.synology.me:8889/md/pbr/zhihu/angles_micro.png)
_微面和渲染片元的角度向量定义_

先放下高光项的公式<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cleft%28%5Cmathrm%7B3%7D%5Cright%29" alt="\left(\mathrm{3}\right)">。首先考虑某个渲染片元（比如是材料表面的一小块且刚好投影到屏幕上的一个像素那么大）这个渲染片元法向量是<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cmathbf%7Bn%7D" alt="\mathbf{n}"> 。和经典的BRDF模型不同的是，也是**微面理论的第一个假设：片元中包含了多个微平面**。因此对于渲染片元来说，最后向观察者<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cmathbf%7Bv%7D" alt="\mathbf{v}">方向传递的光，即辉度（辐射度，radiance）则是其微面辉度的加和：  
![aa](https://goolyuyi.synology.me:8889/md/pbr/zhihu/aa.png)
_对于一个渲染片元来说，观察者方向的辉度可认为是各微面的辉度和_

所以在微面理论中我们按各个微面在<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cmathbf%7Bv%7D" alt="\mathbf{v}">方向投影所占的比例来计算辉度：  

<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=L_%5Cmathbf%7Bo%7D%28%5Cmathbf%7Bv%7D%29%3D%5Cfrac%7B%5Cint%20%5Ctext%20%7B%20projected%20area%20%7D%28x%29%20L%5Cleft%28%5Cmathbf%7Bv%7D%2C%20x%5Cright%29%20d%20x%7D%7B%5Cint%20%5Ctext%20%7B%20projected%20area%20%7D%28x%29%20d%20x%7D%20%20%5Ctag%7B4%7D%5C%5C" alt="L_\mathbf{o}(\mathbf{v})=\frac{\int \text { projected area }(x) L\left(\mathbf{v}, x\right) d x}{\int \text { projected area }(x) d x}  \tag{4}\\">
  
  
同时对于这个单位面积的渲染片元，在观察方向<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cmathbf%7Bv%7D" alt="\mathbf{v}">的投影面积等于：  
![ab](https://goolyuyi.synology.me:8889/md/pbr/zhihu/ab.png)


<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Ctext%20%7B%20projected%20area%20%7D%3D%5Cmathbf%7Bv%7D%20%5Ccdot%20%5Cmathbf%7Bn%7D%3D%5Ccos%20%5Ctheta_%7Bo%7D%20%20%5Ctag%7B5%7D%5C%5C" alt="\text { projected area }=\mathbf{v} \cdot \mathbf{n}=\cos \theta_{o}  \tag{5}\\">
  
  
### 法向面分布函数：  
![ac](https://goolyuyi.synology.me:8889/md/pbr/zhihu/ac.png)


我们需要考虑对于一个单位面积上的渲染片元，朝向<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cmathbf%7Bm%7D" alt="\mathbf{m}">方向上的微面面积，以便我们最后来统计这样的微面所占的比例。于是法向分布函数NDF就是这样定义的：  

<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=D%28%5Cmathbf%7Bm%7D%29%20%3A%3D%5C%7B%5Ctext%7B%E6%9C%9D%E5%90%91%7D%5C%2C%5Cmathbf%7Bm%7D%5C%2C%5Ctext%7B%E7%9A%84%E5%BE%AE%E9%9D%A2%E9%9D%A2%E7%A7%AF%7D%5C%7D%5C%5C" alt="D(\mathbf{m}) :=\{\text{朝向}\,\mathbf{m}\,\text{的微面面积}\}\\">
  
对于NDF有这些属性：  
  
- 不是概率密度函数，也不是正态分布函数（要特别指出这点，被很多文稿弄错），而是一个**面积的密度函数**  
- <img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=0%20%5Cleq%20D%28%5Cmathbf%7Bm%7D%29%20%5Cleq%20%5Cinfty" alt="0 \leq D(\mathbf{m}) \leq \infty">  
- <img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cint%20D%28%5Cmathbf%7Bm%7D%29" alt="\int D(\mathbf{m})">是所有微平面在渲染单元上的面积  
- 所以<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cint%20D%28%5Cmathbf%7Bm%7D%29%20d%20%5Cmathbf%7Bm%7D%5Cgeq%201" alt="\int D(\mathbf{m}) d \mathbf{m}\geq 1">  ，因此等号成立当且仅当渲染片元是一个纯平的面。  
![ad](https://goolyuyi.synology.me:8889/md/pbr/zhihu/ad.png)


以及对于渲染片元法向方向<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cmathbf%7Bn%7D" alt="\mathbf{n}">有：  

<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cint_%7B%5Cmathbf%7Bm%7D%20%5Cin%5COmega%7D%5Cleft%5Clangle%5Cmathbf%7Bm%7D%5Ccdot%5Cmathbf%7Bn%7D%5Cright%5Crangle%20D%28%5Cmathbf%7Bm%7D%29%20d%20%5Cmathbf%7Bm%7D%3D1%5C%5C" alt="\int_{\mathbf{m} \in\Omega}\left\langle\mathbf{m}\cdot\mathbf{n}\right\rangle D(\mathbf{m}) d \mathbf{m}=1\\">
  
  
### 遮挡函数：  
![af](https://goolyuyi.synology.me:8889/md/pbr/zhihu/af.png)


投影的面积不仅和NDF成正比以外，还要考虑微平面被遮挡的情况。如果一个微面是背向观察者或者被其他微面遮挡时，那就不会考虑在<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cleft%28%5Cmathrm%7B4%7D%5Cright%29" alt="\left(\mathrm{4}\right)">式中贡献辉度了。因此我们要定义**其被遮挡的概率函数<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=G_1" alt="G_1">**  

<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=G_1%28%5Cmathbf%7Bm%7D%2C%5Cmathbf%7Bv%7D%29%3A%3D%5C%7B%5Ctext%7B%E5%9C%A8%E8%A7%82%E5%AF%9F%E8%80%85%E6%98%AF%7D%5Cmathbf%7Bv%7D%20%5Ctext%7B%E6%96%B9%E5%90%91%E6%97%B6%7D%EF%BC%8C%5Cmathbf%7Bm%7D%E6%96%B9%E5%90%91%5Ctext%7B%E9%9D%A2%E7%9A%84%E5%8F%AF%E8%A7%81%E6%A6%82%E7%8E%87%7D%5C%7D%5C%5C" alt="G_1(\mathbf{m},\mathbf{v}):=\{\text{在观察者是}\mathbf{v} \text{方向时}，\mathbf{m}方向\text{面的可见概率}\}\\">
  
现在就能计算式中的投影面积了：  

<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Ctext%20%7B%20projected%20area%20%7D%3D%5Cint_%7B%5Cmathbf%7Bm%7D%5Cin%5COmega%7D%20G_%7B1%7D%5Cleft%28%5Cmathbf%7Bv%7D%2C%20%5Cmathbf%7Bm%7D%5Cright%29%5Cleft%3C%5Cmathbf%7Bv%7D%2C%20%5Cmathbf%7Bm%7D%5Cright%3E%20D%5Cleft%28%5Cmathbf%7Bm%7D%5Cright%29%20d%20%5Cmathbf%7Bm%7D%20%20%5Ctag%7B6%7D%5C%5C" alt="\text { projected area }=\int_{\mathbf{m}\in\Omega} G_{1}\left(\mathbf{v}, \mathbf{m}\right)\left<\mathbf{v}, \mathbf{m}\right> D\left(\mathbf{m}\right) d \mathbf{m}  \tag{6}\\">
  
结合<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cleft%28%5Cmathrm%7B5%7D%5Cright%29" alt="\left(\mathrm{5}\right)">式就有了我们的**第一个微面理论的等式**：  

<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Ccos%20%5Ctheta_%7Bo%7D%3D%5Cint_%7B%5COmega%7D%20G_%7B1%7D%5Cleft%28%5Cmathbf%7Bv%7D%2C%20%5Cmathbf%7Bm%7D%5Cright%29%5Cleft%5Clangle%5Cmathbf%7Bv%7D%5Ccdot%20%5Cmathbf%7Bm%7D%5Cright%5Crangle%20D%5Cleft%28%5Cmathbf%7Bm%7D%5Cright%29%20d%20%5Cmathbf%7Bm%7D%5C%5C" alt="\cos \theta_{o}=\int_{\Omega} G_{1}\left(\mathbf{v}, \mathbf{m}\right)\left\langle\mathbf{v}\cdot \mathbf{m}\right\rangle D\left(\mathbf{m}\right) d \mathbf{m}\\">
  
代回<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cleft%28%5Cmathrm%7B4%7D%5Cright%29" alt="\left(\mathrm{4}\right)">式，得到：  

<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=L_%7B%5Cmathbf%7Bo%7D%7D%5Cleft%28%5Cmathbf%7Bv%7D%5Cright%29%3D%5Cfrac%7B1%7D%7B%5Ccos%20%5Ctheta_%7Bo%7D%7D%20%5Cint_%7B%5COmega%7D%20L%5Cleft%28%5Cmathbf%7Bv%7D%2C%20%5Cmathbf%7Bm%7D%5Cright%29%20G_%7B1%7D%5Cleft%28%5Cmathbf%7Bv%7D%2C%20%5Cmathbf%7Bm%7D%5Cright%29%5Cleft%5Clangle%5Cmathbf%7Bv%7D%5Ccdot%20%5Cmathbf%7Bm%7D%5Cright%5Crangle%20D%5Cleft%28%5Cmathbf%7Bm%7D%5Cright%29%20d%20%5Cmathbf%7Bm%7D%20%20%5Ctag%7B7%7D%5C%5C" alt="L_{\mathbf{o}}\left(\mathbf{v}\right)=\frac{1}{\cos \theta_{o}} \int_{\Omega} L\left(\mathbf{v}, \mathbf{m}\right) G_{1}\left(\mathbf{v}, \mathbf{m}\right)\left\langle\mathbf{v}\cdot \mathbf{m}\right\rangle D\left(\mathbf{m}\right) d \mathbf{m}  \tag{7}\\">
  
其中分母的<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cfrac%7B1%7D%7B%5Ccos%20%5Ctheta_%7Bo%7D%7D" alt="\frac{1}{\cos \theta_{o}}">则是<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cleft%28%5Cmathrm%7B4%7D%5Cright%29" alt="\left(\mathrm{4}\right)">式中单位面积渲染片元在观察方向<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cmathbf%7Bv%7D" alt="\mathbf{v}">的投影面积。而积分号下则是对各微面辉度的加和。  
![ag](https://goolyuyi.synology.me:8889/md/pbr/zhihu/ag.png)


此时我们可以定义对于观察方向<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cmathbf%7Bo%7D" alt="\mathbf{o}">的权重函数，以方便后面计算：  

<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=D_%7B%5Cmathbf%7Bm%7D%7D%5Cleft%28%5Cmathbf%7Bm%7D%5Cright%29%3A%3D%5Cfrac%7BG_%7B1%7D%5Cleft%28%5Cmathbf%7Bv%7D%2C%20%5Cmathbf%7Bm%7D%5Cright%29%5Cleft%5Clangle%5Cmathbf%7Bv%7D%5Ccdot%20%5Cmathbf%7Bm%7D%5Cright%5Crangle%20D%5Cleft%28%5Cmathbf%7Bm%7D%5Cright%29%7D%7B%5Ccos%20%5Ctheta_%7Bo%7D%7D%20%5Ctag%7B8%7D%5C%5C" alt="D_{\mathbf{m}}\left(\mathbf{m}\right):=\frac{G_{1}\left(\mathbf{v}, \mathbf{m}\right)\left\langle\mathbf{v}\cdot \mathbf{m}\right\rangle D\left(\mathbf{m}\right)}{\cos \theta_{o}} \tag{8}\\">
  
请留意<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=D_%7B%5Cmathbf%7Bm%7D%7D" alt="D_{\mathbf{m}}">确实是概率密度函数，因为<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cint%20%20%20D_%7B%5Cmathbf%7Bm%7D%7D%28%5Cmathbf%7Bm%7D%29d%5Cmathbf%7Bm%7D%3D1" alt="\int   D_{\mathbf{m}}(\mathbf{m})d\mathbf{m}=1">，所以<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cleft%28%5Cmathrm%7B7%7D%5Cright%29" alt="\left(\mathrm{7}\right)">式可以写成：  

<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=L_%5Cmathbf%7Bo%7D%5Cleft%28%5Cmathbf%7Bv%7D%5Cright%29%3D%5Cint_%7B%5COmega%7D%20L%5Cleft%28%5Cmathbf%7Bv%7D%2C%20%5Cmathbf%7Bm%7D%5Cright%29%20D_%7B%5Cmathbf%7Bm%7D%7D%5Cleft%28%5Cmathbf%7Bm%7D%5Cright%29%20d%20%5Cmathbf%7Bm%7D%20%20%5Ctag%7B9%7D%5C%5C" alt="L_\mathbf{o}\left(\mathbf{v}\right)=\int_{\Omega} L\left(\mathbf{v}, \mathbf{m}\right) D_{\mathbf{m}}\left(\mathbf{m}\right) d \mathbf{m}  \tag{9}\\">
  
  
### 激活面：  
对于<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cleft%28%5Cmathrm%7B9%7D%5Cright%29" alt="\left(\mathrm{9}\right)">式，我们想知道最后的渲染结果<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=L_%5Cmathbf%7Bo%7D%5Cleft%28%5Cmathbf%7Bv%7D%5Cright%29" alt="L_\mathbf{o}\left(\mathbf{v}\right)">，可以对每个积分号下的微面应用**BRDF渲染函数**：  

<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=L_%5Cmathbf%7Bo%7D%28%5Cmathbf%7Bv%7D%29%3D%5Cint_%7B%5Cmathbf%7Bm%7D%5Cin%5COmega%7D%5Cint_%7B%5Cmathbf%7Bl%7D%5Cin%5COmega%7D%20%20%5Crho_%7B%5Cmu%7D%28%5Cmathbf%7Bv%7D%2C%20%5Cmathbf%7Bl%7D%2C%20%5Cmathbf%7Bm%7D%29%20%20L_%5Cmathbf%7Bi%7D%28%5Cmathbf%7Bl%7D%29%20%5Cleft%5Clangle%5Cmathbf%7Bl%7D%5Ccdot%20%5Cmathbf%7Bm%7D%5Cright%5Crangle%20D_%7B%5Cmathbf%7Bm%7D%7D%28%5Cmathbf%7Bm%7D%29%20d%20%5Cmathbf%7Bl%7D%20%5C%2Cd%20%5Cmathbf%7Bm%7D%5C%5C" alt="L_\mathbf{o}(\mathbf{v})=\int_{\mathbf{m}\in\Omega}\int_{\mathbf{l}\in\Omega}  \rho_{\mu}(\mathbf{v}, \mathbf{l}, \mathbf{m})  L_\mathbf{i}(\mathbf{l}) \left\langle\mathbf{l}\cdot \mathbf{m}\right\rangle D_{\mathbf{m}}(\mathbf{m}) d \mathbf{l} \,d \mathbf{m}\\">
  
其中每个微面的BRDF函数是<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Crho_%7B%5Cmu%7D%5Cleft%28%5Cmathbf%7Bv%7D%2C%20%5Cmathbf%7Bl%7D%2C%20%5Cmathbf%7Bm%7D%5Cright%29" alt="\rho_{\mu}\left(\mathbf{v}, \mathbf{l}, \mathbf{m}\right)">。我们在实际渲染过程中是对每一个入射角方向<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cmathbf%7Bl%7D" alt="\mathbf{l}">的光线去求值的，所以我们在这里可以对<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cmathbf%7Bl%7D" alt="\mathbf{l}">进行微分：  

<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=dL_%5Cmathbf%7Bo%7D%28%5Cmathbf%7Bv%7D%29%3DL_%5Cmathbf%7Bi%7D%28%5Cmathbf%7Bl%7D%29%20%5C%2C%20d%20%5Cmathbf%7Bl%7D%20%5Cint_%7B%5Cmathbf%7Bm%7D%5Cin%5COmega%7D%20%5Crho_%7B%5Cmu%7D%28%5Cmathbf%7Bv%7D%2C%20%5Cmathbf%7Bl%7D%2C%20%5Cmathbf%7Bm%7D%29%20%20%5Cleft%5Clangle%5Cmathbf%7Bl%7D%5Ccdot%20%5Cmathbf%7Bm%7D%5Cright%5Crangle%20%20D_%7B%5Cmathbf%7Bm%7D%7D%28%5Cmathbf%7Bm%7D%29%20d%20%5Cmathbf%7Bm%7D%5C%5C" alt="dL_\mathbf{o}(\mathbf{v})=L_\mathbf{i}(\mathbf{l}) \, d \mathbf{l} \int_{\mathbf{m}\in\Omega} \rho_{\mu}(\mathbf{v}, \mathbf{l}, \mathbf{m})  \left\langle\mathbf{l}\cdot \mathbf{m}\right\rangle  D_{\mathbf{m}}(\mathbf{m}) d \mathbf{m}\\">
  
结合<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cleft%28%5Cmathrm%7B2%7D%5Cright%29" alt="\left(\mathrm{2}\right)">式我们就得到一个**在微面理论下关于该渲染片元的BRDF**：  

<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=f%28%5Cmathbf%7Bl%7D%2C%5Cmathbf%7Bv%7D%29%20%3D%20%5Cfrac%7B1%7D%7B%5Cleft%5Clangle%5Cmathbf%7Bl%7D%5Ccdot%5Cmathbf%7Bn%7D%5Cright%5Crangle%7D%5Cint_%7B%5COmega%7D%20%5Crho_%7B%5Cmu%7D%5Cleft%28%5Cmathbf%7Bv%7D%2C%20%5Cmathbf%7Bl%7D%2C%20%5Cmathbf%7Bm%7D%5Cright%29%5Cleft%5Clangle%5Cmathbf%7Bl%7D%5Ccdot%20%5Cmathbf%7Bm%7D%5Cright%5Crangle%20D_%7B%5Cmathbf%7Bm%7D%7D%5Cleft%28%5Cmathbf%7Bm%7D%5Cright%29%20d%20%5Cmathbf%7Bm%7D%20%5Ctag%7B10%7D%5C%5C" alt="f(\mathbf{l},\mathbf{v}) = \frac{1}{\left\langle\mathbf{l}\cdot\mathbf{n}\right\rangle}\int_{\Omega} \rho_{\mu}\left(\mathbf{v}, \mathbf{l}, \mathbf{m}\right)\left\langle\mathbf{l}\cdot \mathbf{m}\right\rangle D_{\mathbf{m}}\left(\mathbf{m}\right) d \mathbf{m} \tag{10}\\">
  
现在我们做出**微面理论的第二个假设：所有贡献高光的微面都是菲涅尔镜面**，所以只有那些和入射光线<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cmathbf%7Bl%7D" alt="\mathbf{l}">和观察方向<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cmathbf%7Bv%7D" alt="\mathbf{v}">的半向量<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cmathbf%7Bh%7D%3D%5Cmathbf%7Bv%7D%2B%5Cmathbf%7Bl%7D" alt="\mathbf{h}=\mathbf{v}+\mathbf{l}"> **完美对齐**的那些微面才会在渲染片元的高光部分起到作用。  
![激活面示意图](https://goolyuyi.synology.me:8889/md/pbr/zhihu/active.png)
_只有刚好对齐了入射光和观察者的半向量h的那些面才会贡献高光部分_

我们把这些起到反射作用的微面称为当前的**激活面**，于是对于右边积分式就只有在<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cmathbf%7Bm%7D%3D%5Cmathbf%7Bh%7D" alt="\mathbf{m}=\mathbf{h}">时有求值的必要(你可以想象成对于半球积分仅当微分角<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=d%5Cmathbf%7Bm%7D" alt="d\mathbf{m}">扫到激活面才不是<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=0" alt="0">），所以我们完全可以把<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Crho_%7B%5Cmu%7D" alt="\rho_{\mu}">用一个[狄拉克函数][Dirac]来代替：  

<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cleft.%5Crho_%7B%5Cmu%7D%5Cleft%28%5Cmathbf%7Bv%7D%2C%20%5Cmathbf%7Bl%7D%2C%20%5Cmathbf%7Bm%7D%5Cright%29%5Cright%7C_%7B%5Cmathbf%7Bm%7D%3D%5Cmathbf%7Bh%7D%7D%3Dk%5C%2C%20%5Cdelta_%7B%5Cmathbf%7Bh%7D%7D%28%5Cmathbf%7Bm%7D%29%5C%5C" alt="\left.\rho_{\mu}\left(\mathbf{v}, \mathbf{l}, \mathbf{m}\right)\right|_{\mathbf{m}=\mathbf{h}}=k\, \delta_{\mathbf{h}}(\mathbf{m})\\">
  
其中：  

<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cdelta_%7Bh%7D%28%5Cmathbf%7Bm%7D%29%20%3A%3D%20%20%5Cbegin%7Bcases%7D%20%20%5Cinfty%20%26%5Ctext%7Bif%20%7D%5C%20%5Cmathbf%7Bm%7D%3D%5Cmathbf%7Bh%7D%5C%5C%20%200%20%26%5Cmathrm%7Botherwise%7D%20%20%5Cend%7Bcases%7D%5C%5C" alt="\delta_{h}(\mathbf{m}) :=  \begin{cases}  \infty &\text{if }\ \mathbf{m}=\mathbf{h}\\  0 &\mathrm{otherwise}  \end{cases}\\">
  
注意这里<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cdelta_%7Bh%7D%28%5Cmathbf%7Bm%7D%29" alt="\delta_{h}(\mathbf{m})">是关于<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cmathbf%7Bm%7D" alt="\mathbf{m}">的狄拉克函数，后面我们积分时要考虑。  
![Dirac函数](https://goolyuyi.synology.me:8889/md/pbr/zhihu/dirac.png)
_狄拉克函数_

同时<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Crho_%7B%5Cmu%7D" alt="\rho_{\mu}">也是菲涅尔镜面，那么对该微面求**半球反射积分**则有：  

<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cbegin%7Baligned%7D%20%20%5Cint_%7B%5Cmathbf%7Bl%7D%5Cin%5COmega%7D%20%5Crho_%7B%5Cmu%7D%5Cleft%28%5Cmathbf%7Bv%7D%2C%20%5Cmathbf%7Bl%7D%2C%5Cmathbf%7Bm%7D%5Cright%29%20%20%5Cleft%5Clangle%5Cmathbf%7Bl%7D%5Ccdot%20%5Cmathbf%7Bm%7D%5Cright%5Crangle%20d%20%5Cmathbf%7Bl%7D%26%20%3D%5Cint_%7B%5Cmathbf%7Bh%7D%5Cin%5COmega%7D%20k%5C%2C%5Cdelta_%7B%5Cmathbf%7Bh%7D%7D%28%5Cmathbf%7Bm%7D%29%20%5Cleft%5C%7C%5Cfrac%7B%5Cpartial%20%5Cmathbf%7Bh%7D%7D%7B%5Cpartial%20%5Cmathbf%7Bl%7D%7D%5Cright%5C%7C%20d%5Cmathbf%7Bl%7D%20%20%5C%5C%5C%5C%26%3D%20F%28%5Ccos%28%5Ctheta_%7Bi%7D%29%29%20%20%5Cend%7Baligned%7D%20%20%5Ctag%7B11%7D%5C%5C" alt="\begin{aligned}  \int_{\mathbf{l}\in\Omega} \rho_{\mu}\left(\mathbf{v}, \mathbf{l},\mathbf{m}\right)  \left\langle\mathbf{l}\cdot \mathbf{m}\right\rangle d \mathbf{l}& =\int_{\mathbf{h}\in\Omega} k\,\delta_{\mathbf{h}}(\mathbf{m}) \left\|\frac{\partial \mathbf{h}}{\partial \mathbf{l}}\right\| d\mathbf{l}  \\\\&= F(\cos(\theta_{i}))  \end{aligned}  \tag{11}\\">
  
要做几点解释：  
  
- <img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=F" alt="F">就是我们熟悉的菲涅尔镜面反射函数，且只有在<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cmathbf%7Bm%7D%3D%5Cmathbf%7Bh%7D" alt="\mathbf{m}=\mathbf{h}">时反光，这里我们用的是<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Ccos%28%5Ctheta_%7Bi%7D%29%3D%5Clangle%5Cmathbf%7Bl%7D%5Ccdot%5Cmathbf%7Bh%7D%5Crangle" alt="\cos(\theta_{i})=\langle\mathbf{l}\cdot\mathbf{h}\rangle">。  
- 微面反射是能量守恒的，且<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=F%20%5Cleq%201" alt="F \leq 1">  
- <img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Crho_%7B%5Cmu%7D" alt="\rho_{\mu}">在等式左边是关于<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cmathbf%7Bl%7D" alt="\mathbf{l}">的函数，在右边是关于<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cmathbf%7Bm%7D" alt="\mathbf{m}">的函数，因此要代入Jacobian系数<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cleft%5C%7C%5Cfrac%7B%5Cpartial%20%5Cmathbf%7Bh%7D%7D%7B%5Cpartial%20%5Cmathbf%7Bl%7D%7D%5Cright%5C%7C" alt="\left\|\frac{\partial \mathbf{h}}{\partial \mathbf{l}}\right\|">  
- 有些文献中积分的是<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=d%5Cmathbf%7Bv%7D" alt="d\mathbf{v}">。这是因为BRDF的[Helmholtz对称性][Helmholtz]即：  

<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=f%28%5Cmathbf%7Bl%7D%2C%20%5Cmathbf%7Bv%7D%29%3Df%28%5Cmathbf%7Bv%7D%2C%20%5Cmathbf%7Bl%7D%29%5C%5C" alt="f(\mathbf{l}, \mathbf{v})=f(\mathbf{v}, \mathbf{l})\\">
  
  
所以**我们积分哪个都是一样的**。  
所以剩下最后的问题就是怎么找到Jacobian系数。要时刻记住微面理论的假设**只有激活面的辉度贡献才不是0**，所以我们只有考虑在这个条件下的计算Jacobian系数  
  
### Jacobian系数推导：  
看到<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cleft%28%5Cmathrm%7B11%7D%5Cright%29" alt="\left(\mathrm{11}\right)">式右边，由于有狄拉克函数的存在，所以只有在积分函数“扫“到<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cmathbf%7Bm%7D%3D%5Cmathbf%7Bh%7D" alt="\mathbf{m}=\mathbf{h}">的时刻，狄拉克函数才不是<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=0" alt="0">。所以我们只需要求此时刻Jacobian系数的<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cleft%5C%7C%5Cfrac%7B%5Cpartial%20%5Cmathbf%7Bh%7D%7D%7B%5Cpartial%20%5Cmathbf%7Bl%7D%7D%5Cright%5C%7C" alt="\left\|\frac{\partial \mathbf{h}}{\partial \mathbf{l}}\right\|"> 值  
我们把此时的向量<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cmathbf%7Bl%7D" alt="\mathbf{l}">移到向量<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cmathbf%7Bv%7D" alt="\mathbf{v}">的末端，令<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cmathbf%7Bh_s%7D%3D%5Cmathbf%7Bl%7D%2B%5Cmathbf%7Bv%7D" alt="\mathbf{h_s}=\mathbf{l}+\mathbf{v}">。根据前面的描述，此时的<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cmathbf%7Bh%7D" alt="\mathbf{h}">正好是和<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cmathbf%7Bh_s%7D" alt="\mathbf{h_s}">方向一致的单位向量。  
![jacobian1](https://goolyuyi.synology.me:8889/md/pbr/zhihu/jacobian1.png)


我们再来考虑此时的<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5CDelta%7B%5Cmathbf%7Bl%7D%7D" alt="\Delta{\mathbf{l}}">  
![jacobian2](https://goolyuyi.synology.me:8889/md/pbr/zhihu/jacobian2.png)


对于此时刻的<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5CDelta%7B%5Cmathbf%7Bh_s%7D%7D" alt="\Delta{\mathbf{h_s}}">和<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5CDelta%7B%5Cmathbf%7Bl%7D%7D" alt="\Delta{\mathbf{l}}">有如下关系：  
![jacobian3](https://goolyuyi.synology.me:8889/md/pbr/zhihu/jacobian3.png)


也就是：  

<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%7C%5CDelta%7B%5Cmathbf%7Bh_s%7D%7D%7C%3D%7C%5Cmathbf%7Bh%7D%5Ccdot%5Cmathbf%7Bl%7D%7C%7C%5CDelta%7B%5Cmathbf%7Bl%7D%7D%7C%5C%5C" alt="|\Delta{\mathbf{h_s}}|=|\mathbf{h}\cdot\mathbf{l}||\Delta{\mathbf{l}}|\\">
  
因此对于<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cmathbf%7Bh%7D" alt="\mathbf{h}">有：  

<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%7C%5CDelta%7B%5Cmathbf%7Bh%7D%7D%7C%3D%5Cfrac%7B%7C%5Cmathbf%7Bh%7D%5Ccdot%5Cmathbf%7Bl%7D%7C%7D%7B%5C%7C%5Cmathbf%7Bh_s%7D%5C%7C%5E2%7D%7C%5CDelta%7B%5Cmathbf%7Bl%7D%7D%7C%5Ctag%7B12%7D%5C%5C" alt="|\Delta{\mathbf{h}}|=\frac{|\mathbf{h}\cdot\mathbf{l}|}{\|\mathbf{h_s}\|^2}|\Delta{\mathbf{l}}|\tag{12}\\">
  
然后：  

<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cbegin%7Baligned%7D%20%20%7C%7C%5Cmathbf%7Bh_s%7D%7C%7C%26%3D%7C%28%5Cmathbf%7Bl%7D%2B%5Cmathbf%7Bv%7D%29%5Ccdot%5Cmathbf%7Bh%7D%7C%20%20%5C%5C%5C%5C%26%3D%7C2%5Cmathbf%7Bh%7D%5Ccdot%5Cmathbf%7Bl%7D%7C%20%20%5Cend%7Baligned%7D%5C%5C" alt="\begin{aligned}  ||\mathbf{h_s}||&=|(\mathbf{l}+\mathbf{v})\cdot\mathbf{h}|  \\\\&=|2\mathbf{h}\cdot\mathbf{l}|  \end{aligned}\\">
  

<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%7C%7C%5Cmathbf%7Bh_s%7D%7C%7C%5E2%3D4%5C%2C%7C%5Cmathbf%7Bh%7D%5Ccdot%5Cmathbf%7Bl%7D%7C%5E2%5C%5C" alt="||\mathbf{h_s}||^2=4\,|\mathbf{h}\cdot\mathbf{l}|^2\\">
  
代入<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cleft%28%5Cmathrm%7B12%7D%5Cright%29" alt="\left(\mathrm{12}\right)">式，稍作整理并求<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5CDelta%5Cmathbf%7Bh%7D/%5CDelta%5Cmathbf%7Bl%7D" alt="\Delta\mathbf{h}/\Delta\mathbf{l}">的极限，则有：  

<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cleft%5C%7C%5Cfrac%7B%5Cpartial%20%5Cmathbf%7Bh%7D%7D%7B%5Cpartial%20%5Cmathbf%7Bl%7D%7D%5Cright%5C%7C%3D%5Cfrac%7B1%7D%7B4%5Cleft%7C%5Cmathbf%7Bl%7D%20%5Ccdot%20%5Cmathbf%7Bh%7D%5Cright%7C%7D%5C%5C" alt="\left\|\frac{\partial \mathbf{h}}{\partial \mathbf{l}}\right\|=\frac{1}{4\left|\mathbf{l} \cdot \mathbf{h}\right|}\\">
  
  
### PBR的高光项公式：  
我们最后求的这个系数是：<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cleft%5C%7C%5Cfrac%7B%5Cpartial%20%5Cmathbf%7Bh%7D%7D%7B%5Cpartial%20%5Cmathbf%7Bl%7D%7D%5Cright%5C%7C%3D%5Cfrac%7B1%7D%7B4%5Cleft%7C%5Cmathbf%7Bl%7D%20%5Ccdot%20%5Cmathbf%7Bh%7D%5Cright%7C%7D" alt="\left\|\frac{\partial \mathbf{h}}{\partial \mathbf{l}}\right\|=\frac{1}{4\left|\mathbf{l} \cdot \mathbf{h}\right|}">，回到<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cleft%28%5Cmathrm%7B11%7D%5Cright%29" alt="\left(\mathrm{11}\right)">式，狄拉克函数和积分号是可以消去了，所以我们的激活面BRDF是：  

<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cbegin%7Baligned%7D%20%5Crho_%7B%5Cmu%7D%5Cleft%28%5Cmathbf%7Bv%7D%2C%5Cmathbf%7Bl%7D%2C%5Cmathbf%7Bm%7D%5Cright%29%20%20%26%3D%20%20%5Cleft%5C%7C%5Cfrac%7B%5Cpartial%20%5Cmathbf%7Bh%7D%7D%7B%5Cpartial%20%5Cmathbf%7Bl%7D%7D%5Cright%5C%7C%20%20%5Cfrac%7BF%5Cleft%28%5Cmathbf%7Bv%7D%5Ccdot%20%5Cmathbf%7Bh%7D%5Cright%29%20%5Cdelta_%7B%5Cmathbf%7Bh%7D%7D%5Cleft%28%5Cmathbf%7Bm%7D%5Cright%29%7D%7B%5Cleft%7C%5Cmathbf%7Bl%7D%20%5Ccdot%20%5Cmathbf%7Bh%7D%5Cright%7C%7D%20%5C%5C%20%26%20%20%3D%5Cfrac%7BF%5Cleft%28%5Cmathbf%7Bv%7D%5Ccdot%20%5Cmathbf%7Bh%7D%5Cright%29%20%5Cdelta_%7B%5Cmathbf%7Bh%7D%7D%5Cleft%28%5Cmathbf%7Bm%7D%5Cright%29%7D%7B4%5Cleft%7C%5Cmathbf%7Bl%7D%20%5Ccdot%20%5Cmathbf%7Bh%7D%5Cright%7C%5E%7B2%7D%7D%20%5Cend%7Baligned%7D%5C%5C" alt="\begin{aligned} \rho_{\mu}\left(\mathbf{v},\mathbf{l},\mathbf{m}\right)  &=  \left\|\frac{\partial \mathbf{h}}{\partial \mathbf{l}}\right\|  \frac{F\left(\mathbf{v}\cdot \mathbf{h}\right) \delta_{\mathbf{h}}\left(\mathbf{m}\right)}{\left|\mathbf{l} \cdot \mathbf{h}\right|} \\ &  =\frac{F\left(\mathbf{v}\cdot \mathbf{h}\right) \delta_{\mathbf{h}}\left(\mathbf{m}\right)}{4\left|\mathbf{l} \cdot \mathbf{h}\right|^{2}} \end{aligned}\\">
  
太好了，绕了一大圈我们终于可以代回<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cleft%28%5Cmathrm%7B10%7D%5Cright%29" alt="\left(\mathrm{10}\right)">式了，可以得到我们在微面理论下渲染片元的BRDF：  

<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=f%28%5Cmathbf%7Bl%7D%2C%5Cmathbf%7Bv%7D%29%20%3D%20%5Cfrac%7B1%7D%7B%5Cleft%5Clangle%5Cmathbf%7Bl%7D%5Ccdot%5Cmathbf%7Bn%7D%5Cright%5Crangle%7D%5Cint_%7B%5COmega%7D%20%5Cfrac%7BF%5Cleft%28%5Cmathbf%7Bv%7D%2C%20%5Cmathbf%7Bh%7D%5Cright%29%20%5Cdelta_%7B%5Cmathbf%7Bh%7D%7D%5Cleft%28%5Cmathbf%7Bm%7D%5Cright%29%7D%7B4%5Cleft%7C%5Cmathbf%7Bl%7D%20%5Ccdot%20%5Cmathbf%7Bh%7D%5Cright%7C%5E%7B2%7D%7D%20%20%5Cleft%5Clangle%5Cmathbf%7Bl%7D%5Ccdot%20%5Cmathbf%7Bm%7D%5Cright%5Crangle%20D_%7B%5Cmathbf%7Bm%7D%7D%28%5Cmathbf%7Bm%7D%29%20d%20%5Cmathbf%7Bm%7D%5C%5C" alt="f(\mathbf{l},\mathbf{v}) = \frac{1}{\left\langle\mathbf{l}\cdot\mathbf{n}\right\rangle}\int_{\Omega} \frac{F\left(\mathbf{v}, \mathbf{h}\right) \delta_{\mathbf{h}}\left(\mathbf{m}\right)}{4\left|\mathbf{l} \cdot \mathbf{h}\right|^{2}}  \left\langle\mathbf{l}\cdot \mathbf{m}\right\rangle D_{\mathbf{m}}(\mathbf{m}) d \mathbf{m}\\">
  
根据<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cleft%28%5Cmathrm%7B8%7D%5Cright%29" alt="\left(\mathrm{8}\right)">式，把<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=D_%7B%5Cmathbf%7Bm%7D%7D%28%5Cmathbf%7Bm%7D%29" alt="D_{\mathbf{m}}(\mathbf{m})">展开：  

<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cbegin%7Baligned%7D%20%20f%28%5Cmathbf%7Bl%7D%2C%5Cmathbf%7Bv%7D%29%20%26%3D%20%5Cfrac%7B1%7D%7B%5Cleft%5Clangle%5Cmathbf%7Bl%7D%5Ccdot%20%5Cmathbf%7Bn%7D%5Cright%5Crangle%7D%20%20%5Cint_%7B%5Cmathbf%7Bm%7D%5Cin%5COmega%7D%20%5Cfrac%7BF%5Cleft%28%5Cmathbf%7Bv%7D%5Ccdot%20%5Cmathbf%7Bh%7D%5Cright%29%20%5Cdelta_%7B%5Cmathbf%7Bh%7D%7D%5Cleft%28%5Cmathbf%7Bm%7D%5Cright%29%7D%7B4%5Cleft%7C%5Cmathbf%7Bl%7D%20%5Ccdot%20%5Cmathbf%7Bh%7D%5Cright%7C%5E%7B2%7D%7D%20%20%5Cleft%5Clangle%5Cmathbf%7Bl%7D%5Ccdot%20%5Cmathbf%7Bm%7D%5Cright%5Crangle%20%20%5Cfrac%7BG_%7B1%7D%5Cleft%28%5Cmathbf%7Bv%7D%5Ccdot%20%5Cmathbf%7Bm%7D%5Cright%29%5Cleft%5Clangle%5Cmathbf%7Bv%7D%5Ccdot%20%5Cmathbf%7Bm%7D%5Cright%5Crangle%20D%5Cleft%28%5Cmathbf%7Bm%7D%5Cright%29%7D%7B%5Cleft%5Clangle%5Cmathbf%7Bv%7D%5Ccdot%20%5Cmathbf%7Bn%7D%5Cright%5Crangle%7D%20d%20%5Cmathbf%7Bm%7D%20%20%5C%5C%5C%5C%20%20%26%3D%7B%7D%20%20%5Cfrac%7BF%5Cleft%28%5Cmathbf%7Bv%7D%5Ccdot%20%5Cmathbf%7Bh%7D%5Cright%29%20%7D%7B4%5Cleft%5Clangle%5Cmathbf%7Bl%7D%5Ccdot%20%5Cmathbf%7Bn%7D%5Cright%5Crangle%5Cleft%7C%5Cmathbf%7Bl%7D%20%5Ccdot%20%5Cmathbf%7Bh%7D%5Cright%7C%5E%7B2%7D%7D%20%20%5Cleft%5Clangle%5Cmathbf%7Bl%7D%5Ccdot%20%5Cmathbf%7Bh%7D%5Cright%5Crangle%20%20%5Cfrac%7BG_%7B1%7D%5Cleft%28%5Cmathbf%7Bv%7D%5Ccdot%20%5Cmathbf%7Bh%7D%5Cright%29%5Cleft%5Clangle%5Cmathbf%7Bv%7D%5Ccdot%20%5Cmathbf%7Bh%7D%5Cright%5Crangle%20D%5Cleft%28%5Cmathbf%7Bh%7D%5Cright%29%7D%7B%5Cleft%5Clangle%5Cmathbf%7Bv%7D%5Ccdot%20%5Cmathbf%7Bn%7D%5Cright%5Crangle%7D%20%20%5Cend%7Baligned%7D%5C%5C" alt="\begin{aligned}  f(\mathbf{l},\mathbf{v}) &= \frac{1}{\left\langle\mathbf{l}\cdot \mathbf{n}\right\rangle}  \int_{\mathbf{m}\in\Omega} \frac{F\left(\mathbf{v}\cdot \mathbf{h}\right) \delta_{\mathbf{h}}\left(\mathbf{m}\right)}{4\left|\mathbf{l} \cdot \mathbf{h}\right|^{2}}  \left\langle\mathbf{l}\cdot \mathbf{m}\right\rangle  \frac{G_{1}\left(\mathbf{v}\cdot \mathbf{m}\right)\left\langle\mathbf{v}\cdot \mathbf{m}\right\rangle D\left(\mathbf{m}\right)}{\left\langle\mathbf{v}\cdot \mathbf{n}\right\rangle} d \mathbf{m}  \\\\  &={}  \frac{F\left(\mathbf{v}\cdot \mathbf{h}\right) }{4\left\langle\mathbf{l}\cdot \mathbf{n}\right\rangle\left|\mathbf{l} \cdot \mathbf{h}\right|^{2}}  \left\langle\mathbf{l}\cdot \mathbf{h}\right\rangle  \frac{G_{1}\left(\mathbf{v}\cdot \mathbf{h}\right)\left\langle\mathbf{v}\cdot \mathbf{h}\right\rangle D\left(\mathbf{h}\right)}{\left\langle\mathbf{v}\cdot \mathbf{n}\right\rangle}  \end{aligned}\\">
  
因为<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cleft%5Clangle%5Cmathbf%7Bl%7D%5Ccdot%5Cmathbf%7B%20h%7D%5Cright%5Crangle%3D%5Cleft%5Clangle%5Cmathbf%7Bv%7D%5Ccdot%5Cmathbf%7Bh%7D%5Cright%5Crangle" alt="\left\langle\mathbf{l}\cdot\mathbf{ h}\right\rangle=\left\langle\mathbf{v}\cdot\mathbf{h}\right\rangle">最后则有：  

<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=f%28%5Cmathbf%7Bl%7D%2C%5Cmathbf%7Bv%7D%29%20%3D%5Cfrac%7BF%5Cleft%28%5Cmathbf%7Bv%7D%2C%20%5Cmathbf%7Bh%7D%5Cright%29%20G_%7B1%7D%5Cleft%28%5Cmathbf%7Bv%7D%2C%20%5Cmathbf%7Bh%7D%5Cright%29%20D%5Cleft%28%5Cmathbf%7Bh%7D%5Cright%29%7D%7B4%5Cleft%7C%5Cmathbf%7Bn%7D%20%5Ccdot%20%5Cmathbf%7Bv%7D%5Cright%7C%5Cleft%7C%5Cmathbf%7Bn%7D%20%5Ccdot%20%5Cmathbf%7Bl%7D%5Cright%7C%7D%5C%5C" alt="f(\mathbf{l},\mathbf{v}) =\frac{F\left(\mathbf{v}, \mathbf{h}\right) G_{1}\left(\mathbf{v}, \mathbf{h}\right) D\left(\mathbf{h}\right)}{4\left|\mathbf{n} \cdot \mathbf{v}\right|\left|\mathbf{n} \cdot \mathbf{l}\right|}\\">
  
  
  
## Smith遮挡阴影函数  
在微面理论中的**第三个假设是：每一个微面的法向和位置都是独立的（independent）**，虽然这个假设和实际情况略有不同，即实际情况更准确应该微面是自相关（autocorrelation）的。但在实际应用中我们发现仍然能非常好的拟合现实的数据。  
![ba](https://goolyuyi.synology.me:8889/md/pbr/zhihu/ba.png)
_真实情况下的微面是一个随机过程，autocorrelation不为0（左图）
为了推出Smith G1函数，需要假设每一个微面高度和朝向都是不相关的（右图）_

那么对于<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=G_%7B1%7D%28%5Cmathbf%7Bv%7D%2C%20%5Cmathbf%7Bm%7D%29" alt="G_{1}(\mathbf{v}, \mathbf{m})"> 函数，除了在<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cmathbf%7Bm%7D" alt="\mathbf{m}">是背向<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cmathbf%7Bv%7D" alt="\mathbf{v}">的情况以外，对于<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cmathbf%7Bm%7D" alt="\mathbf{m}">也是不依赖的  
我们现在回到上面的<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cleft%28%5Cmathrm%7B6%7D%5Cright%29" alt="\left(\mathrm{6}\right)">式，积分号那里开始，我们把和<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cmathbf%7Bm%7D" alt="\mathbf{m}">不依赖的遮挡函数定义为<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=G1%5E%2B" alt="G1^+">：  

<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cbegin%7Baligned%7D%20%26%5Cint_%7B%5COmega%7D%20G_%7B1%7D%5Cleft%28%5Cmathbf%7Bv%7D%2C%20%5Cmathbf%7Bm%7D%5Cright%29%5Cleft%5Clangle%5Cmathbf%7Bv%7D%5Ccdot%20%5Cmathbf%7Bm%7D%5Cright%5Crangle%20D%5Cleft%28%5Cmathbf%7Bm%7D%5Cright%29%20d%20%5Cmathbf%7Bm%7D%20%5C%5C%5C%5C%26%5Cqquad%3D%5Cfrac%7B%5Cint_%7B%5COmega%7D%20%5Cchi%5E%7B%2B%7D%5Cleft%28%5Cmathbf%7Bv%7D%20%5Ccdot%20%5Cmathbf%7Bm%7D%5Cright%29%20G_%7B1%7D%5Cleft%28%5Cmathbf%7Bv%7D%2C%20%5Cmathbf%7Bm%7D%5Cright%29%20d%20%5Cmathbf%7Bm%7D%7D%7B%5Cint_%7B%5COmega%7D%20%5Cchi%5E%7B%2B%7D%5Cleft%28%5Cmathbf%7Bv%7D%20%5Ccdot%20%5Cmathbf%7Bm%7D%5Cright%29%20d%20%5Cmathbf%7Bm%7D%7D%20%5Cint_%7B%5COmega%7D%5Cleft%5Clangle%5Cmathbf%7Bv%7D%5Ccdot%20%5Cmathbf%7Bm%7D%5Cright%5Crangle%20D%5Cleft%28%5Cmathbf%7Bm%7D%5Cright%29%20d%20%5Cmathbf%7Bm%7D%20%5C%5C%5C%5C%26%5Cqquad%3DG_%7B1%7D%5E%7B%2B%7D%5Cleft%28%5Cmathbf%7Bv%7D%5Cright%29%20%5Cint_%7B%5COmega%7D%5Cleft%5Clangle%5Cmathbf%7Bv%7D%5Ccdot%20%5Cmathbf%7Bm%7D%5Cright%5Crangle%20D%5Cleft%28%5Cmathbf%7Bm%7D%5Cright%29%20d%20%5Cmathbf%7Bm%7D%20%5Cend%7Baligned%7D%20%5Ctag%7B13%7D%5C%5C" alt="\begin{aligned} &\int_{\Omega} G_{1}\left(\mathbf{v}, \mathbf{m}\right)\left\langle\mathbf{v}\cdot \mathbf{m}\right\rangle D\left(\mathbf{m}\right) d \mathbf{m} \\\\&\qquad=\frac{\int_{\Omega} \chi^{+}\left(\mathbf{v} \cdot \mathbf{m}\right) G_{1}\left(\mathbf{v}, \mathbf{m}\right) d \mathbf{m}}{\int_{\Omega} \chi^{+}\left(\mathbf{v} \cdot \mathbf{m}\right) d \mathbf{m}} \int_{\Omega}\left\langle\mathbf{v}\cdot \mathbf{m}\right\rangle D\left(\mathbf{m}\right) d \mathbf{m} \\\\&\qquad=G_{1}^{+}\left(\mathbf{v}\right) \int_{\Omega}\left\langle\mathbf{v}\cdot \mathbf{m}\right\rangle D\left(\mathbf{m}\right) d \mathbf{m} \end{aligned} \tag{13}\\">
  
这里要解释几点：

- 因为<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=G1%5E%2B%28%5Cmathbf%7Bv%7D%29" alt="G1^+(\mathbf{v})">独立于<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cmathbf%7Bm%7D" alt="\mathbf{m}">，所以也就不用写在积分号下了。  
- <img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cchi%5E%7B%2B%7D" alt="\chi^{+}">是[Heaviside阶跃函数][Heaviside]  
![Heaviside](https://goolyuyi.synology.me:8889/md/pbr/zhihu/heaviside.png)
_阶跃函数_

因此我们计算的<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=G_%7B1%7D%5E%7B%2B%7D" alt="G_{1}^{+}">其实是计算的是**没有被遮挡面的平均值**：  

<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=G_%7B1%7D%5E%7B%2B%7D%5Cleft%28%5Cmathbf%7Bv%7D%5Cright%29%3D%5Cfrac%7B%5Cint_%7B%5COmega%7D%20%5Cchi%5E%7B%2B%7D%5Cleft%28%5Cmathbf%7Bv%7D%20%5Ccdot%20%5Cmathbf%7Bm%7D%5Cright%29%20G_%7B1%7D%5Cleft%28%5Cmathbf%7Bv%7D%2C%20%5Cmathbf%7Bm%7D%5Cright%29%20d%20%5Cmathbf%7Bm%7D%7D%7B%5Cint_%7B%5COmega%7D%20%5Cchi%5E%7B%2B%7D%5Cleft%28%5Cmathbf%7Bv%7D%20%5Ccdot%20%5Cmathbf%7Bm%7D%5Cright%29%20d%20%5Cmathbf%7Bm%7D%7D%5C%5C" alt="G_{1}^{+}\left(\mathbf{v}\right)=\frac{\int_{\Omega} \chi^{+}\left(\mathbf{v} \cdot \mathbf{m}\right) G_{1}\left(\mathbf{v}, \mathbf{m}\right) d \mathbf{m}}{\int_{\Omega} \chi^{+}\left(\mathbf{v} \cdot \mathbf{m}\right) d \mathbf{m}}\\">
  
结合<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cleft%28%5Cmathrm%7B13%7D%5Cright%29" alt="\left(\mathrm{13}\right)">式：  

<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Ccos%20%5Ctheta_%7Bo%7D%3DG_%7B1%7D%5E%7B%2B%7D%5Cleft%28%5Cmathbf%7Bv%7D%5Cright%29%20%5Cint_%7B%5COmega%7D%5Cleft%5Clangle%5Cmathbf%7Bm%7D%5Ccdot%20%5Cmathbf%7Bv%7D%5Cright%5Crangle%20D%5Cleft%28%5Cmathbf%7Bm%7D%5Cright%29%20d%20%5Cmathbf%7Bm%7D%5C%5C" alt="\cos \theta_{o}=G_{1}^{+}\left(\mathbf{v}\right) \int_{\Omega}\left\langle\mathbf{m}\cdot \mathbf{v}\right\rangle D\left(\mathbf{m}\right) d \mathbf{m}\\">
  
所以：  

<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=G_%7B1%7D%5E%7B%2B%7D%5Cleft%28%5Cmathbf%7Bv%7D%5Cright%29%3D%5Cfrac%7B%5Ccos%20%5Ctheta_%7Bo%7D%7D%7B%5Cint_%7B%5COmega%7D%5Cleft%5Clangle%5Cmathbf%7Bv%7D%2C%20%5Cmathbf%7Bm%7D%5Cright%5Crangle%20D%5Cleft%28%5Cmathbf%7Bm%7D%5Cright%29%20d%20%5Cmathbf%7Bm%7D%7D%5C%5C" alt="G_{1}^{+}\left(\mathbf{v}\right)=\frac{\cos \theta_{o}}{\int_{\Omega}\left\langle\mathbf{v}, \mathbf{m}\right\rangle D\left(\mathbf{m}\right) d \mathbf{m}}\\">
  
但最后，因为对于背向<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cmathbf%7Bv%7D" alt="\mathbf{v}">的那些面应该是不考虑的，所以我们还要引入阶跃函数：  

<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cbegin%7Baligned%7D%20%20G_%7B1%7D%5Cleft%28%5Cmathbf%7Bv%7D%2C%20%5Cmathbf%7Bm%7D%5Cright%29%26%3D%5Cchi%5E%7B%2B%7D%5Cleft%28%5Cmathbf%7Bv%7D%20%5Ccdot%20%5Cmathbf%7Bm%7D%5Cright%29G_%7B1%7D%5E%7B%2B%7D%5Cleft%28%5Cmathbf%7Bv%7D%5Cright%29%20%5C%5C%5C%5C%26%3D%5Cchi%5E%7B%2B%7D%5Cleft%28%5Cmathbf%7Bv%7D%20%5Ccdot%20%5Cmathbf%7Bm%7D%5Cright%29%20%5Cfrac%7B%5Ccos%20%5Ctheta_%7Bo%7D%7D%7B%5Cint_%7B%5COmega%7D%5Cleft%5Clangle%5Cmathbf%7Bv%7D%5Ccdot%20%5Cmathbf%7Bm%7D%5Cright%5Crangle%20D%5Cleft%28%5Cmathbf%7Bm%7D%5Cright%29%20d%20%5Cmathbf%7Bm%7D%7D%20%20%5Cend%7Baligned%7D%20%5Ctag%7B14%7D%5C%5C" alt="\begin{aligned}  G_{1}\left(\mathbf{v}, \mathbf{m}\right)&=\chi^{+}\left(\mathbf{v} \cdot \mathbf{m}\right)G_{1}^{+}\left(\mathbf{v}\right) \\\\&=\chi^{+}\left(\mathbf{v} \cdot \mathbf{m}\right) \frac{\cos \theta_{o}}{\int_{\Omega}\left\langle\mathbf{v}\cdot \mathbf{m}\right\rangle D\left(\mathbf{m}\right) d \mathbf{m}}  \end{aligned} \tag{14}\\">
  
  
### Smith遮挡函数：  
对于很多PBR模型中（比如GGX和Beckmann）都会使用Smith遮挡函数。这个函数就是我们刚刚推导在<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cleft%28%5Cmathrm%7B14%7D%5Cright%29" alt="\left(\mathrm{14}\right)">式的函数，只是我们把积分域从法向<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cmathbf%7Bv%7D" alt="\mathbf{v}">换到了斜率空间<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cmu" alt="\mu">了而已：  

<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=G_%7B1%7D%5Cleft%28%5Cmathbf%7Bv%7D%2C%20%5Cmathbf%7Bm%7D%5Cright%29%3D%5Cfrac%7B%5Cchi%5E%7B%2B%7D%5Cleft%28%5Cmathbf%7Bv%7D%20%5Ccdot%20%5Cmathbf%7Bm%7D%5Cright%29%7D%7B1%2B%5CLambda%5Cleft%28a%5Cright%29%7D%5Ctag%7B15%7D%5C%5C" alt="G_{1}\left(\mathbf{v}, \mathbf{m}\right)=\frac{\chi^{+}\left(\mathbf{v} \cdot \mathbf{m}\right)}{1+\Lambda\left(a\right)}\tag{15}\\">
  
其中<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=a" alt="a">是向量<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cmathbf%7Bv%7D" alt="\mathbf{v}">的斜率<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cmu%3D%5Cleft%7C%5Ccot%20%5Ctheta_%7Bv%7D%5Cright%7C" alt="\mu=\left|\cot \theta_{v}\right|">，而<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5CLambda%5Cleft%28a%5Cright%29" alt="\Lambda\left(a\right)">和式一样也是一个由<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=D%5Cleft%28%5Cmathbf%7Bm%7D%5Cright%29" alt="D\left(\mathbf{m}\right)">决定的函数。（具体的推导过程篇幅很长，并且与我们理解概念没有多大关系，所以具体想了解可以可以参考有关推导）  
我们可以看到在式<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cleft%28%5Cmathrm%7B14%7D%5Cright%29" alt="\left(\mathrm{14}\right)">和式<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cleft%28%5Cmathrm%7B15%7D%5Cright%29" alt="\left(\mathrm{15}\right)">，且在第三个假设的前提下是**精确的（Exact）**。  
  
### 阴影遮挡函数：  
![阴影遮挡](https://goolyuyi.synology.me:8889/md/pbr/zhihu/shadowmask.png)
_微面不仅可能被遮挡（中图），还可能被阴影（左图），实际情况还会在微面中多次反射（右图）_

回到<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cleft%28%5Cmathrm%7B6%7D%5Cright%29" alt="\left(\mathrm{6}\right)">式，之前只考虑了遮挡情况。然而实际上除了在<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cmathbf%7Bv%7D" alt="\mathbf{v}">方向微面有被遮挡的情况，**在光射入的<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cmathbf%7Bl%7D" alt="\mathbf{l}">方向也有微面在阴影中的情况**，因此我们在实际使用的是阴影遮挡函数<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=G_2" alt="G_2">。对于<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=G_2" alt="G_2">函数在我们已经可以求得Smith遮挡函数的前提下，有以下几种模型：  
  
#### 阴影和遮挡函数不相关：  
这是最早提出的，认为阴影和遮挡是不相关（independent）的，因此总会比实际微面被阴影/遮挡的值要大，会在渲染材质时显得更暗。  

<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cbegin%7Baligned%7D%20G_%7B2%7D%5Cleft%28%5Cmathbf%7Bv%7D%2C%20%5Cmathbf%7Bl%7D%2C%20%5Cmathbf%7Bm%7D%5Cright%29%20%26%3DG_%7B1%7D%5Cleft%28%5Cmathbf%7Bv%7D%2C%20%5Cmathbf%7Bm%7D%5Cright%29%20G_%7B1%7D%5Cleft%28%5Cmathbf%7Bl%7D%2C%20%5Cmathbf%7Bm%7D%5Cright%29%20%5C%5C%20%26%3D%5Cfrac%7B%5Cchi%5E%7B%2B%7D%5Cleft%28%5Cmathbf%7Bv%7D%20%5Ccdot%20%5Cmathbf%7Bm%7D%5Cright%29%7D%7B1%2B%5CLambda%5Cleft%28%5Cmathbf%7Bv%7D%5Cright%29%7D%20%5Cfrac%7B%5Cchi%5E%7B%2B%7D%5Cleft%28%5Cmathbf%7Bl%7D%20%5Ccdot%20%5Cmathbf%7Bm%7D%5Cright%29%7D%7B1%2B%5CLambda%5Cleft%28%5Cmathbf%7Bl%7D%5Cright%29%7D%20%5Cend%7Baligned%7D%5C%5C" alt="\begin{aligned} G_{2}\left(\mathbf{v}, \mathbf{l}, \mathbf{m}\right) &=G_{1}\left(\mathbf{v}, \mathbf{m}\right) G_{1}\left(\mathbf{l}, \mathbf{m}\right) \\ &=\frac{\chi^{+}\left(\mathbf{v} \cdot \mathbf{m}\right)}{1+\Lambda\left(\mathbf{v}\right)} \frac{\chi^{+}\left(\mathbf{l} \cdot \mathbf{m}\right)}{1+\Lambda\left(\mathbf{l}\right)} \end{aligned}\\">
  
  
#### 阴影遮挡函数是在微面高度上相关：  
这个模型考虑了微面高度对阴影遮挡的相关性（correlation），高度越高的微面被遮挡/阴影或者同时被阴影遮挡的概率就越小，因此在近似精确度上已经远好于上一个模型了：  

<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=G_%7B2%7D%5Cleft%28%5Cmathbf%7Bv%7D%2C%20%5Cmathbf%7Bl%7D%2C%20%5Cmathbf%7Bm%7D%5Cright%29%3D%5Cfrac%7B%5Cchi%5E%7B%2B%7D%5Cleft%28%5Cmathbf%7Bv%7D%20%5Ccdot%20%5Cmathbf%7Bm%7D%5Cright%29%20%5Cchi%5E%7B%2B%7D%5Cleft%28%5Cmathbf%7Bl%7D%20%5Ccdot%20%5Cmathbf%7Bm%7D%5Cright%29%7D%7B1%2B%5CLambda%5Cleft%28%5Cmathbf%7Bv%7D%5Cright%29%2B%5CLambda%5Cleft%28%5Cmathbf%7Bl%7D%5Cright%29%7D%5C%5C" alt="G_{2}\left(\mathbf{v}, \mathbf{l}, \mathbf{m}\right)=\frac{\chi^{+}\left(\mathbf{v} \cdot \mathbf{m}\right) \chi^{+}\left(\mathbf{l} \cdot \mathbf{m}\right)}{1+\Lambda\left(\mathbf{v}\right)+\Lambda\left(\mathbf{l}\right)}\\">
  
  
#### 阴影遮挡函数是在微面法向上相关：  
这个模型考虑的是如果光线方向<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cmathbf%7Bl%7D" alt="\mathbf{l}">和视线方向<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cmathbf%7Bv%7D" alt="\mathbf{v}">夹脚越小的话，那么阴影和遮挡相关性就越高。在极限情况时，阴影/遮挡函数就**完全相关了（full correlation）**。  
实际上在<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cmathbf%7Bl%7D" alt="\mathbf{l}">和<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cmathbf%7Bv%7D" alt="\mathbf{v}">的<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cmathrm%7Bazimuthal%7D" alt="\mathrm{azimuthal}">角一致的情况下，阴影遮挡函数就是完全相关的。所以我们可以考虑把<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cmathrm%7Bazimuthal%7D" alt="\mathrm{azimuthal}">角<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cphi" alt="\phi">作为参数：  

<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cbegin%7Barray%7D%7Bl%7D%7BG_%7B2%7D%5Cleft%28%5Cmathbf%7Bv%7D%2C%20%5Cmathbf%7Bl%7D%2C%20%5Cmathbf%7Bm%7D%5Cright%29%7D%20%5C%5C%20%7B%3D%5Clambda%28%5Cphi%29%20G_%7B1%7D%5Cleft%28%5Cmathbf%7Bv%7D%2C%20%5Cmathbf%7Bm%7D%5Cright%29%20G_%7B1%7D%5Cleft%28%5Cmathbf%7Bl%7D%2C%20%5Cmathbf%7Bm%7D%5Cright%29%2B%281-%5Clambda%28%5Cphi%29%29%20%5Cmin%20%5Cleft%28G_%7B1%7D%5Cleft%28%5Cmathbf%7Bv%7D%2C%20%5Cmathbf%7Bm%7D%5Cright%29%2C%20G_%7B1%7D%5Cleft%28%5Cmathbf%7Bl%7D%2C%20%5Cmathbf%7Bm%7D%5Cright%29%5Cright%29%7D%5Cend%7Barray%7D%5C%5C" alt="\begin{array}{l}{G_{2}\left(\mathbf{v}, \mathbf{l}, \mathbf{m}\right)} \\ {=\lambda(\phi) G_{1}\left(\mathbf{v}, \mathbf{m}\right) G_{1}\left(\mathbf{l}, \mathbf{m}\right)+(1-\lambda(\phi)) \min \left(G_{1}\left(\mathbf{v}, \mathbf{m}\right), G_{1}\left(\mathbf{l}, \mathbf{m}\right)\right)}\end{array}\\">
  
其中<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Clambda%28%5Cphi%29" alt="\lambda(\phi)">是一个经验函数，在下面会讲到  
  
#### 阴影遮挡函数在微面高度和法向上都是相关的：  
同时考虑到两种相关性，因此也是最好的近似：  

<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=G_%7B2%7D%5Cleft%28%5Cmathbf%7Bv%7D%2C%20%5Cmathbf%7Bl%7D%2C%20%5Cmathbf%7Bm%7D%5Cright%29%3D%5Cfrac%7B%5Cchi%5E%7B%2B%7D%5Cleft%28%5Cmathbf%7Bv%7D%20%5Ccdot%20%5Cmathbf%7Bm%7D%5Cright%29%20%5Cchi%5E%7B%2B%7D%5Cleft%28%5Cmathbf%7Bl%7D%20%5Ccdot%20%5Cmathbf%7Bm%7D%5Cright%29%7D%7B1%2B%5Cmax%20%5Cleft%28%5CLambda%5Cleft%28%5Cmathbf%7Bv%7D%5Cright%29%2C%20%5CLambda%5Cleft%28%5Cmathbf%7Bl%7D%5Cright%29%5Cright%29%2B%5Clambda%5Cleft%28%5Cmathbf%7Bv%7D%2C%20%5Cmathbf%7Bl%7D%5Cright%29%20%5Cmin%20%5Cleft%28%5CLambda%5Cleft%28%5Cmathbf%7Bv%7D%5Cright%29%2C%20%5CLambda%5Cleft%28%5Cmathbf%7Bl%7D%5Cright%29%5Cright%29%7D%5C%5C" alt="G_{2}\left(\mathbf{v}, \mathbf{l}, \mathbf{m}\right)=\frac{\chi^{+}\left(\mathbf{v} \cdot \mathbf{m}\right) \chi^{+}\left(\mathbf{l} \cdot \mathbf{m}\right)}{1+\max \left(\Lambda\left(\mathbf{v}\right), \Lambda\left(\mathbf{l}\right)\right)+\lambda\left(\mathbf{v}, \mathbf{l}\right) \min \left(\Lambda\left(\mathbf{v}\right), \Lambda\left(\mathbf{l}\right)\right)}\\">
  
和仅高度相关的函数一样，也有一个关于<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cmathrm%7Bazimuthal%7D" alt="\mathrm{azimuthal}">角的函数<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Clambda%28%5Cphi%29" alt="\lambda(\phi)">，这个函数目前我们只能提供经验模型：  

<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Clambda%3D%5Cfrac%7B4.41%20%5Cphi%7D%7B4.41%20%5Cphi%2B1%7D%20%5Ctag%7B16%7D%5C%5C" alt="\lambda=\frac{4.41 \phi}{4.41 \phi+1} \tag{16}\\">
  
  
## 形状不变性与Roughness  
对于一个渲染片元，我们想象将其拉伸（Stretching），如图：  
![ca](https://goolyuyi.synology.me:8889/md/pbr/zhihu/ca.png)


图中我们仅是一个一维空间的渲染片元。拉伸操作**不会改变微面的拓扑结构**，而且我们连观察向量<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cmathbf%7Bv%7D" alt="\mathbf{v}">也一起拉伸的话，拉伸后阴影遮挡概率也是不变的。  然而对于微面的斜率分部函数，实际上是正好相反**收缩**的。如果微面的斜率分部改变了，相应地，法向概率分布函数<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=D%28%5Cmathbf%7Bm%7D%29" alt="D(\mathbf{m})">也会改变。微面法向分布越集中就越光滑。这就是我们可以通过**拉伸/收缩微面分部来控制渲染片元粗糙程度（Roughness）的原因**！  
![Roughness示例](https://goolyuyi.synology.me:8889/md/pbr/zhihu/roughness.png)
_通过roughness/smoothness控制材质表面_

因此我们定义粗糙程度参数为<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Calpha" alt="\alpha">，这个参数就是我们拉伸/收缩渲染片元的比例。从上面的图我们也能看出，对于观察方向<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cmathbf%7Bl%7D" alt="\mathbf{l}">的斜率在此时和<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Calpha" alt="\alpha">的关系则为：  

<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=a%3D%5Cfrac%7B1%7D%7B%5Calpha%20%5Ctan%20%5Ctheta_%7Bo%7D%7D%5C%5C" alt="a=\frac{1}{\alpha \tan \theta_{o}}\\">
  
**后面我们把只依赖粗糙程度<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Calpha" alt="\alpha">，而观察方向<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=a" alt="a">是由<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Calpha" alt="\alpha">决定的情况，定义为形状不变（shape invariant）**  
对于**有形状不变假设的BRDF**（比如：Beckmann，GGX）比起没有的（比如：Phong，GTR），有以下优势：  
  
- 可以推导出各向异性的NDF和<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=G" alt="G">函数，用于渲染各项异性材质（关于各项异性材质渲染在后续文稿里再做介绍）。  
- Smith <img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=G" alt="G">函数是建立在形状不变性假设上的，也因此只有形状不变的BRDF才有<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=G" alt="G">函数（关于NDF）的解析式，而像Phong模型是没有<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=G" alt="G">的解析式。  
- 无论是<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=G" alt="G">还是NDF函数，只依赖唯一个变量<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=a" alt="a">，可查表求值（比如像Unity的内建shader就是这样做的），能提高运算效率。  
  
## 基于PBR的BRDF  
**相信你能看到这里真的很了不起**！一开始，我们从显微镜下观察到了物体的微面结构，然后做出了微面理论的三个假设，一步一步的用光学和几何学知识做为基础，推导出了基于微面理论的PBR模型。  
![推导PBR示例](https://goolyuyi.synology.me:8889/md/pbr/zhihu/bigeqn.png)


在我们总结之前，需要完成我们高光项的最后形态，也就是把式中的遮挡函数<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=G_1" alt="G_1">替换成式的<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=G_2" alt="G_2">函数：  

<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=f%28%5Cmathbf%7Bl%7D%2C%5Cmathbf%7Bv%7D%29%20%3D%5Cfrac%7BF%5Cleft%28%5Cmathbf%7Bv%7D%2C%20%5Cmathbf%7Bh%7D%5Cright%29%20G_%7B2%7D%5Cleft%28%5Cmathbf%7Bv%7D%2C%20%5Cmathbf%7Bh%7D%5Cright%29%20D%5Cleft%28%5Cmathbf%7Bh%7D%5Cright%29%7D%7B4%5Cleft%7C%5Cmathbf%7Bn%7D%20%5Ccdot%20%5Cmathbf%7Bv%7D%5Cright%7C%5Cleft%7C%5Cmathbf%7Bn%7D%20%5Ccdot%20%5Cmathbf%7Bl%7D%5Cright%7C%7D%5C%5C" alt="f(\mathbf{l},\mathbf{v}) =\frac{F\left(\mathbf{v}, \mathbf{h}\right) G_{2}\left(\mathbf{v}, \mathbf{h}\right) D\left(\mathbf{h}\right)}{4\left|\mathbf{n} \cdot \mathbf{v}\right|\left|\mathbf{n} \cdot \mathbf{l}\right|}\\">
  
  
### 现在我们可以来总结前面的推导了：  
![展示图](https://goolyuyi.synology.me:8889/md/pbr/zhihu/desney.jpg)
_迪士尼电影：无敌破坏王2，使用PBR渲染的主角_

- PBR的BRDF和经典的BRDF一样，把渲染式分为**高光项和漫反射项**。  
- 和经典BRDF一样，PBR把**漫反射用一个兰伯特平面近似**。  
- 不同于经典BRDF，PBR把**高光项用多个微小菲涅尔平面近似（即微面理论）**，使得高光项也同样具有物理意义。因此PBR是能量守恒的。  
- PBR的高光项具有两个输入参数：<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=F_0" alt="F_0">表示材质的直接反光能力（通常在渲染器中也叫做Metallic），可参考[上一篇]。粗糙程度（Roughness）<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Calpha" alt="\alpha">，用于调整物体表面光滑程度。在很多渲染引擎中会换算成高光度（Specular）和光泽度（Glossiness）两个参数  
![Param](https://goolyuyi.synology.me:8889/md/pbr/zhihu/param.png)
_目前渲染器实现都支持roughness/metallical或者specular/glossiness_

- 菲涅尔反射函数<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=F%5Cleft%28%5Cmathbf%7Bv%7D%2C%20%5Cmathbf%7Bh%7D%5Cright%29" alt="F\left(\mathbf{v}, \mathbf{h}\right)">项，通常用  

<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=F%28%5Cmathbf%7Bn%7D%2C%201%29%20%5Capprox%20F_%7B0%7D%2B%5Cleft%281-F_%7B0%7D%5Cright%29%5Cleft%281-%28%5Cmathbf%7Bn%7D%20%5Ccdot%201%29%5E%7B%2B%7D%5Cright%29%5E%7B5%7D%5C%5C" alt="F(\mathbf{n}, 1) \approx F_{0}+\left(1-F_{0}\right)\left(1-(\mathbf{n} \cdot 1)^{+}\right)^{5}\\">
  
来近似，或者使用LUT查表求值。  
- 分母项是用来归一化（normalized）的，和早期的Cook Torrence高光项很相似只是把<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cpi" alt="\pi">换成了<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=4" alt="4">  
- 法向面分布函数<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=D" alt="D">项表示关于法向的微面面积。对于不同的渲染材质（Material），有不同的<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=D" alt="D">函数。所以对于不同的材质，要么实际测量其微面分布，然后**拟合**其<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=D" alt="D">函数（比如皮肤），要么通过几何模型进行数学建模（比如布料）求出<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=D" alt="D">的解析式。  
![Cloth](https://goolyuyi.synology.me:8889/md/pbr/zhihu/cloth.png)
_用几何建模实现的布料渲染_

- 遮挡函数<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=G_1" alt="G_1">项表示微面在观察方向被遮挡的概率。因为有2个自由度而且是和<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=D" alt="D">函数相关的，所以很难求出。而如果是用Smith遮挡函数，那么<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=G_1" alt="G_1">函数不再依赖微面朝向，所以在已知<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=D" alt="D">函数的情况下可以直接解出。  
- 实际模型中我们应该使用阴影遮挡函数<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=G_2" alt="G_2">，<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=G_2" alt="G_2">是同时依赖观察者的遮挡和光线射入两个<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=G_1" alt="G_1">函数的，而且<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=G_2" alt="G_2">函数是会考虑两个<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=G_1" alt="G_1">函数的相关性的。  
- 如果<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=G_1" alt="G_1">和<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=D" alt="D">只依赖粗糙程度<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Calpha" alt="\alpha">，而不依赖观察方向，那么BRDF是**形状不变**的。改变<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Calpha" alt="\alpha">不会改变微面的拓扑结构和阴影遮挡情况，也就不会改变材质的性质（Property）。  
- PBR的BRDF也是没考虑子表面散射（Subsurface Scattering）的情况，所以也不能模拟折射（refraction）或透射（transmit）效果。  
![sss](https://goolyuyi.synology.me:8889/md/pbr/zhihu/sss.jpg)
_模拟子表面散射现象（图中红框所示）在PBR的模型下需要另外使用专门算法（ad-hoc）_

### BRDF基准测试  
我们对于一个BRDF模型很重要的标准是：**是否能量守恒**。在考虑一个材质表面没有透射（因为BRDF无法模拟这种情况），同时也假设材料不吸收任何输入光时，能量是否守恒：  

<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cint_%7B%5COmega%7D%20f%5Cleft%28%5Cmathbf%7Bl%7D%2C%20%5Cmathbf%7Bv%7D%5Cright%29%5Cleft%7C%5Cmathbf%7Bn%7D%20%5Ccdot%20%5Cmathbf%7Bl%7D%5Cright%7C%20d%20%5Cmathbf%3D1%5C%5C" alt="\int_{\Omega} f\left(\mathbf{l}, \mathbf{v}\right)\left|\mathbf{n} \cdot \mathbf{l}\right| d \mathbf=1\\">
  
这个测试叫做**白炉测试（White Furnace Test）**，可以理解为一束照度（irrandiance）为<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=1" alt="1">的光从上往下照到材料表面（没有阴影）：  
![white furnace ea](https://goolyuyi.synology.me:8889/md/pbr/zhihu/ea.png)
_光从法线方向照下来，没有投影的，所以不用考虑阴影情况_

此时外面空间上有个光幕罩住了整个表面，我们要测试的就是**整个光幕收集到的光照度和是否为<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=1" alt="1">**：  
![white furnace ed](https://goolyuyi.synology.me:8889/md/pbr/zhihu/ed.png)
_白炉测试考虑所有反射出的光_

但遗憾的是我们的微面模型BRDF并没有模拟蓝色向量中这种多次反射的现象（事实上是会被阴影遮挡函数<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=G_2" alt="G_2">遮挡），所以**是不可能通过白炉测试**：  
![white furnace ec](https://goolyuyi.synology.me:8889/md/pbr/zhihu/ec.png)
_在被遮挡的情况下，白炉测试除了纯平的表面是不可能为1的_

这也是理论上**基于微面理论下的BRDF会比实际暗一点**的原因。  
但我们如果使用<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=G_1" alt="G_1">函数，前面我们的推导就能表明：  

<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cint_%7B%5COmega%7D%20%5Crho%5Cleft%28%5Cmathbf%7Bv%7D%2C%20%5Cmathbf%7Bl%7D%5Cright%29%5Cleft%7C%5Cmathbf%7Bn%7D%20%5Ccdot%20%5Cmathbf%7Bl%7D%5Cright%7C%20d%20%5Cmathbf%7Bl%7D%3D%5Cint_%7B%5COmega%7D%20%5Cfrac%7BG_%7B1%7D%5Cleft%28%5Cmathbf%7Bh%7D%2C%20%5Cmathbf%7Bv%7D%5Cright%29%20D%5Cleft%28%5Cmathbf%7Bh%7D%5Cright%29%7D%7B4%5Cleft%7C%5Cmathbf%7Bn%7D%20%5Ccdot%20%5Cmathbf%7Bv%7D%5Cright%7C%7D%20d%20%5Cmathbf%7Bl%7D%3D1%5C%5C" alt="\int_{\Omega} \rho\left(\mathbf{v}, \mathbf{l}\right)\left|\mathbf{n} \cdot \mathbf{l}\right| d \mathbf{l}=\int_{\Omega} \frac{G_{1}\left(\mathbf{h}, \mathbf{v}\right) D\left(\mathbf{h}\right)}{4\left|\mathbf{n} \cdot \mathbf{v}\right|} d \mathbf{l}=1\\">
  
所以我们把能通过这种测试的BRDF模型称为**弱白炉测试**：  
![white furnace eb](https://goolyuyi.synology.me:8889/md/pbr/zhihu/eb.png)
_弱白炉测试，不再考虑遮挡情况_

### Smith遮挡函数的实用性  
其实在历史上还存在另一个BRDF模型能通过弱白炉测试测试：V-cavity BRDF，最初的想法是通过若干不同尺度的V型表面来近似渲染材质：  
![V-cavity](https://goolyuyi.synology.me:8889/md/pbr/zhihu/vcavity.png)
_用多个V形表面去模拟材质_

而对于基于NDF的微面模型，自从G1函数被提出后很多年以后，我们才找出Smith遮挡函数，是的其通过弱白炉测试。  
即使整个图形学历史上只有基于NDF的微面模型以及V-cavity模型是同时能证明通过弱白炉测试且在数学上精确的。但V-cavity模型由于不像微面模型依赖NDF分布函数，使得其实际渲染效果表现的非常糟糕，并没有什么实际的用处。  
![V-cavity2](https://goolyuyi.synology.me:8889/md/pbr/zhihu/vcavity_bad.png)
_在不同的粗糙程度下，V-cavity模型（左列）的反射lobe比起Smith遮挡和NDF函数（中列）效果要差，参考蒙特卡洛光线跟踪算法（右列）_

因此为什么在几乎所有的PBR渲染模型中（比如GGX）都使用Smith遮挡函数，就是因为其在假设的前提下是**数学精确的且能量守恒的**。而对于**Smith遮挡函数的物理可行性和使用正态分布这两个优点都是我们推导过程中的副产品**。  
  
## 已实现的PBR  
这里我们主要会介绍三种BRDF实现：Beckmann，Phong，GGX  
Phong是基于经验模型开发的，Beckmann是在假设了高斯正态分布表面（gaussian rough surface）的前提下推导的模型，而GGX是目前使用最广泛的模型。[Real Time Rendering 4th]上也提到过GGX最初的提出者是[Trowbridge and Reitz]，只是后来被Disney公司命名为GGX，所以我们这里也特别提出来向原作者致敬！  
![PBR Impl](https://goolyuyi.synology.me:8889/md/pbr/zhihu/playerone.jpg)
_电影：头号玩家_

### Beckmann：  

<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=D%5Cleft%28%5Cmathbf%7Bm%7D%5Cright%29%20%3D%5Cfrac%7B%5Cchi%5E%7B%2B%7D%5Cleft%28%5Cmathbf%7Bm%7D%20%5Ccdot%20%5Cmathbf%7Bn%7D%5Cright%29%7D%7B%5Cpi%20%5Calpha%5E%7B2%7D%20%5Ccos%20%5E%7B4%7D%20%5Ctheta_%7Bm%7D%7D%20%5Cexp%20%5Cleft%28-%5Cfrac%7B%5Ctan%20%5E%7B2%7D%20%5Ctheta_%7Bm%7D%7D%7B%5Calpha%5E%7B2%7D%7D%5Cright%29%5C%5C" alt="D\left(\mathbf{m}\right) =\frac{\chi^{+}\left(\mathbf{m} \cdot \mathbf{n}\right)}{\pi \alpha^{2} \cos ^{4} \theta_{m}} \exp \left(-\frac{\tan ^{2} \theta_{m}}{\alpha^{2}}\right)\\">
  

<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5CLambda%5Cleft%28%5Cmathbf%7Bv%7D%5Cright%29%20%3D%5Cfrac%7B%5Coperatorname%7Berf%7D%28a%29-1%7D%7B2%7D%2B%5Cfrac%7B1%7D%7B2%20a%20%5Csqrt%7B%5Cpi%7D%7D%20%5Cexp%20%5Cleft%28-a%5E%7B2%7D%5Cright%29%20%5Ctag%7B17%7D%5C%5C" alt="\Lambda\left(\mathbf{v}\right) =\frac{\operatorname{erf}(a)-1}{2}+\frac{1}{2 a \sqrt{\pi}} \exp \left(-a^{2}\right) \tag{17}\\">
  
其中

<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=a%3D%5Cfrac%7B1%7D%7B%5Calpha%20%5Ctan%20%5Ctheta_%7Bo%7D%7D%5C%5C" alt="a=\frac{1}{\alpha \tan \theta_{o}}\\">
  

<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=G_%7B1%7D%5Cleft%28%5Cmathbf%7Bv%7D%2C%20%5Cmathbf%7Bm%7D%5Cright%29%3D%5Cfrac%7B%5Cchi%5E%7B%2B%7D%5Cleft%28%5Cmathbf%7Bv%7D%20%5Ccdot%20%5Cmathbf%7Bm%7D%5Cright%29%7D%7B1%2B%5CLambda%5Cleft%28%5Cmathbf%7Bv%7D%5Cright%29%7D%5C%5C" alt="G_{1}\left(\mathbf{v}, \mathbf{m}\right)=\frac{\chi^{+}\left(\mathbf{v} \cdot \mathbf{m}\right)}{1+\Lambda\left(\mathbf{v}\right)}\\">
  
对于<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5CLambda%5Cleft%28%5Cmathbf%7Bv%7D%5Cright%29" alt="\Lambda\left(\mathbf{v}\right)">会包含[误差函数]（error function），求值很麻烦，所以我们可以用如下公式近似：  

<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5CLambda%5Cleft%28%5Cmathbf%7Bv%7D%5Cright%29%20%5Capprox%20%5Cleft%5C%7B%5Cbegin%7Barray%7D%7Bll%7D%7B%5Cfrac%7B1-1.259%20a%2B0.396%20a%5E%7B2%7D%7D%7B3.533%20a%2B2.181%20a%5E%7B2%7D%7D%7D%20%26%20%7B%5Ctext%20%7B%20if%20%7D%20a%3C1.6%7D%20%5C%5C%20%7B0%7D%20%26%20%7B%5Ctext%20%7B%20otherwise%20%7D%7D%5Cend%7Barray%7D%5Cright.%20%5Ctag%7B18%7D%5C%5C" alt="\Lambda\left(\mathbf{v}\right) \approx \left\{\begin{array}{ll}{\frac{1-1.259 a+0.396 a^{2}}{3.533 a+2.181 a^{2}}} & {\text { if } a<1.6} \\ {0} & {\text { otherwise }}\end{array}\right. \tag{18}\\">
  
  
### GGX：  

<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cbegin%7Baligned%7D%20D%5Cleft%28%5Cmathbf%7Bm%7D%5Cright%29%20%26%3D%5Cfrac%7B%5Cchi%5E%7B%2B%7D%5Cleft%28%5Cmathbf%7Bm%7D%20%5Ccdot%20%5Cmathbf%7Bn%7D%5Cright%29%7D%7B%5Cpi%20%5Calpha%5E%7B2%7D%20%5Ccos%20%5E%7B4%7D%20%5Ctheta_%7Bm%7D%5Cleft%281%2B%5Cfrac%7B%5Ctan%20%5E%7B2%7D%20%5Ctheta_%7Bm%7D%7D%7B%5Calpha%5E%7B2%7D%7D%5Cright%29%5E%7B2%7D%7D%20%5C%5C%20%5CLambda%5Cleft%28%5Cmathbf%7Bv%7D%5Cright%29%20%26%3D%5Cfrac%7B-1%2B%5Csqrt%7B1%2B%5Cfrac%7B1%7D%7Ba%5E%7B2%7D%7D%7D%7D%7B2%7D%20%5Cend%7Baligned%7D%5C%5C" alt="\begin{aligned} D\left(\mathbf{m}\right) &=\frac{\chi^{+}\left(\mathbf{m} \cdot \mathbf{n}\right)}{\pi \alpha^{2} \cos ^{4} \theta_{m}\left(1+\frac{\tan ^{2} \theta_{m}}{\alpha^{2}}\right)^{2}} \\ \Lambda\left(\mathbf{v}\right) &=\frac{-1+\sqrt{1+\frac{1}{a^{2}}}}{2} \end{aligned}\\">
  
其中  

<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=a%3D%5Cfrac%7B1%7D%7B%5Calpha%20%5Ctan%20%5Ctheta_%7Bo%7D%7D%5C%5C" alt="a=\frac{1}{\alpha \tan \theta_{o}}\\">
  
以及  

<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=G_%7B1%7D%5Cleft%28%5Cmathbf%7Bv%7D%2C%20%5Cmathbf%7Bm%7D%5Cright%29%3D%5Cfrac%7B%5Cchi%5E%7B%2B%7D%5Cleft%28%5Cmathbf%7Bv%7D%20%5Ccdot%20%5Cmathbf%7Bm%7D%5Cright%29%7D%7B1%2B%5CLambda%5Cleft%28%5Cmathbf%7Bv%7D%5Cright%29%7D%5C%5C" alt="G_{1}\left(\mathbf{v}, \mathbf{m}\right)=\frac{\chi^{+}\left(\mathbf{v} \cdot \mathbf{m}\right)}{1+\Lambda\left(\mathbf{v}\right)}\\">
  
  
### Phong/Blinn：  
由于Phong在计算机渲染领域曾经是最重要的模型，虽然现在已经差不多抛弃了，但我们还是给出Phong模型在PBR下的式子：  

<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=D%28%5Cmathbf%7Bm%7D%29%3D%5Cchi%5E%7B%2B%7D%28%5Cmathbf%7Bn%7D%20%5Ccdot%20%5Cmathbf%7Bm%7D%29%20%5Cfrac%7B%5Calpha_%7Bp%7D%2B2%7D%7B2%20%5Cpi%7D%28%5Cmathbf%7Bn%7D%20%5Ccdot%20%5Cmathbf%7Bm%7D%29%5E%7B%5Calpha_%7Bp%7D%7D%5C%5C" alt="D(\mathbf{m})=\chi^{+}(\mathbf{n} \cdot \mathbf{m}) \frac{\alpha_{p}+2}{2 \pi}(\mathbf{n} \cdot \mathbf{m})^{\alpha_{p}}\\">
  
为了使得粗糙程度参数调整上比较均匀，我们用<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Calpha_b" alt="\alpha_b">控制粗糙程度，因此和<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Calpha_p" alt="\alpha_p">的关系是：  

<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Calpha_%7Bp%7D%3D2%20%5Calpha_%7Bb%7D%5E%7B-2%7D-2%5C%5C" alt="\alpha_{p}=2 \alpha_{b}^{-2}-2\\">
  
然而在PBR下的Phong模型是有一些缺陷的：一是Phong**不是形状不变的**，所以在调整粗糙程度时会改变微面分布情况。而另一个是<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5CLambda%5Cleft%28%5Cmathbf%7Bv%7D%5Cright%29" alt="\Lambda\left(\mathbf{v}\right)">没有解析式，我们可以令<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=a%3D%5Csqrt%7B0.5%20%5Calpha_%7Bp%7D%2B1%7D%20/%5Cleft%28%5Ctan%20%5Ctheta_%7Bo%7D%5Cright%29" alt="a=\sqrt{0.5 \alpha_{p}+1} /\left(\tan \theta_{o}\right)">，然后用Beckmann（<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cleft%28%5Cmathrm%7B17%7D%5Cright%29" alt="\left(\mathrm{17}\right)">式或<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cleft%28%5Cmathrm%7B18%7D%5Cright%29" alt="\left(\mathrm{18}\right)">式）代替。这时Phong和Beckmann模型的表现是非常接近的  
![GGxBeckmannPhong](https://goolyuyi.synology.me:8889/md/pbr/zhihu/GGXBeckmannPhong.png)
_在和反射向量呈不同角度高光光线密度，上图中蓝色虚线是Phong/Blinn模型，绿色实线是Beckmann模型，红色实线是GGX模型
下图中，上行是Phong和Beckmann模型的渲染效果，下行是GGX的渲染效果，可以看出GGX渲染高光处出现了"光晕"_

### PBR模型评价：  
现在我们来考察这几种模型在微面分布<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=D" alt="D">上的区别。对于Phong和Beckmann其微面分布是基本一致的，所以渲染结果基本也一致。而对于GGX，对比起Beckmann来，分布图上会多出了一条“尾巴“，这使得GGX在实际渲染高光时是随着粗糙程度增加而呈现光晕效果的。  
究竟哪个模型更好，由于篇幅，我们在这里只给出结论：**GGX更接近现实的情况**。  
![GGXvsPhong](https://goolyuyi.synology.me:8889/md/pbr/zhihu/GGXvsPhong.png)
_GGX模型和Phong/Blinn模型的比较_

所以由于GGX模型在计算量和近似程度上都当之无愧是目前使用范围最广的模型。  
  
## PBR之后  
![PBR_daniel](https://goolyuyi.synology.me:8889/md/pbr/zhihu/daniel-bystedt-treecreature-eevee-render-1.jpg)
_使用Blender渲染引擎渲染，图片来自[艺术家Daniel Bystedt](https://www.artstation.com/artwork/oL4Dq)_

终于，不辞千辛万苦，我们算是彻底的理解了PBR是如何工作的！  
在讨论完PBR，去大干一场之前我们再来看看目前PBR的一些发展方向：  
![real micro](https://goolyuyi.synology.me:8889/md/pbr/zhihu/realmicro.png)
_左为真实情况时的NDF表面，右为PBR模型下的NDF表面_

- 能否在不做出**第三个假设**前提下，推导出一个类似Smith遮挡函数的方案。因为实际中，微面都是自相关（autocorrect）的，而Smith遮挡函数的近似就会过于理想。  
- 对于**Smith遮挡函数的闭解析式**目前只找到了Beckmann和GGX的，而对于更好的GGX的泛化模型GTR还没有找到，这使得GTR模型无法得到有效使用。  
- 对于遮挡阴影函数<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5Cleft%28%5Cmathrm%7B16%7D%5Cright%29" alt="\left(\mathrm{16}\right)">式，我们还只能使用**经验模型**，对于**推导出数学精确模型**一直都受到关注。  
![lobe](https://goolyuyi.synology.me:8889/md/pbr/zhihu/lobe.jpg)
_Pixar的RenderMan实现的SpecRough Lobe_

- 能否在介于完全镜面反射的高光项和完全漫反射的漫反射项之间再创造出一个**额外的高光反射项（specular lobe）**，以解决目前过于复杂的PBR模型推导。  
  
最后我也真诚的建议你去阅读一下这几年SIGGRAPH的重头戏，有关PBR的一些应用或研究：  
https://blog.selfshadow.com/publications/s2017-shading-course/  
  
## 作者后记
这是我第一篇真正完成的技术系列，前后做了很多尝试都未能满意，绞尽脑汁完成后又觉得意犹未尽。突然间想起了安静的躺在加州博物馆里的这只犹他茶壶（相信如果从事图形学工作的人一定不会陌生吧）。
![utar](https://goolyuyi.synology.me:8889/md/pbr/zhihu/utar.png)
_收藏在计算机历史博物馆里犹他茶壶_

谁能想到这只普通的不得了的茶壶却是如今这个充满想象的虚拟世界的开端。作为一名独立研究者，独立游戏制作者，除了平时默默耕耘外，也希望在喜欢的事情上开个好头！也欢迎和我一样喜欢研究技术，或者对艺术热爱的你，疯狂的骚扰我吧！
![表情](https://goolyuyi.synology.me:8889/md/pbr/zhihu/avatar.png)
_goolyuyi，微博：@goolyuyi_

- 虽然Phong模型也有微面理论的假设，但仍然是一个经验模型  
- 渲染片元，这里理解为要渲染某个物体表明上的一小块，在实时渲染中对应于屏幕上一块像素的渲染  
- 这里要特别申明一下，后面的数学公式为了书写方便，其中即使<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5CLambda" alt="\Lambda">函数输入的是一个向量，比如<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5CLambda%28%5Cmathbf%7Bv%7D%29" alt="\Lambda(\mathbf{v})">，也表示输入的是该向量的斜率，即<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex=%5CLambda%28%5Ccot%28%7B%5Ctheta_%7Bo%7D%7D%29%29" alt="\Lambda(\cot({\theta_{o}}))">。  
- [Real Time Rendering 4th]第9章：Physically Based Shading主要是介绍了PBR的BRDF的结论  
- 在光学的描述使用辉度（光辉）更为准确，而不是使用辐射学的辐照度  
- Trowbridge, T. S., and K. P. Reitz, “Average Irregularity Representation of a Roughened Surface for Ray Reﬂection,”Appendix A  
  
[学习课程]:https://blog.selfshadow.com/publications/s2017-shading-course/  
  
[Real Time Rendering 4th]:http://www.realtimerendering.com/  
  
[Trowbridge and Reitz]:https://www.osapublishing.org/josa/abstract.cfm?uri=josa-65-5-531  
[上一篇]: aaa  
[经验模型]:https://en.wikipedia.org/wiki/Empirical_relationship  
[误差函数]:https://en.wikipedia.org/wiki/Error_function  
[Helmholtz]:https://en.wikipedia.org/wiki/Helmholtz_reciprocity  
[Dirac]:https://en.wikipedia.org/wiki/Dirac_delta_function  
[Heaviside]:https://en.wikipedia.org/wiki/Heaviside_step_function  
  
*[CG]:Computer Graphics
