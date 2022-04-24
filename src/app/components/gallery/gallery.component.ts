import { DataServiceService } from './../../services/data-service.service';
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router, NavigationEnd } from '@angular/router';
import { images_data } from 'src/database';

@Component({
  selector: 'app-gallery',
  templateUrl: './gallery.component.html',
  styleUrls: ['./gallery.component.sass']
})
export class GalleryComponent implements OnInit {

  images_data = images_data
  current_route = 'newcomers'
  current_route_id = 0
  dataSet : any = null
  current_article = 0

  constructor(private router : Router, private route: ActivatedRoute, private dataService : DataServiceService) {
    dataService.getData(this.current_route).subscribe(data=>{
      this.dataSet = data.message
      console.log(this.dataSet)
    })
    router.events.subscribe((val)=>{
      if(val instanceof NavigationEnd){
        if (this.current_route != this.route.snapshot.url[0].path){
          this.current_route = this.route.snapshot.url[0].path
          for(let i = 0; i<this.images_data.length; i+=1){
            if(this.images_data[i].category==this.current_route){
              this.current_route_id = i
              dataService.getData(this.current_route).subscribe(data=>{
                data = data
                console.log(data)
              })
              
            }     
          }
        }
      }
    })
   }
  

  ngOnInit(): void {
    // onInitFunction()
    window.onload = function () {
      let newHeight = 30
      let i = 0
      let lastIndex = 4
      let parallax_types = ['parallaxSlow', 'parallaxMedium', 'parallaxHigh']
      document.querySelectorAll<HTMLElement>(".imageCard").forEach(element => {
        
        element.style.visibility = 'visible'
        element.classList.add('animate__fadeInUp')

        let newHorizontalChange = Math.floor(Math.random() * 7)+4; 
        if (i%2 == 0){
          newHorizontalChange = 0-newHorizontalChange
        }    
        newHeight+=(Math.floor(Math.random() * 30));
        element.setAttribute('style', `position:relative; top:${newHeight}px; right:${newHorizontalChange}vw`)
        window.addEventListener('scroll',function(){
          var value = 0- window.scrollY + newHeight;
          
          if (element.classList.contains('parallaxHigh')){
            let movingSpeed = value*0.14
            element.style.top = `${movingSpeed}px`
          }
          else if (element.classList.contains('parallaxMedium')){
            let movingSpeed = value*0.08
            element.style.top = `${movingSpeed}px`
          }
          else if (element.classList.contains('parallaxSlow')){
            let movingSpeed = value*0.04
            element.style.top = `${movingSpeed}px`
          }
        })
        let randomIndex = Math.floor(Math.random() * 3)
        while(randomIndex == lastIndex){
          randomIndex = Math.floor(Math.random() * 3)
        }
        lastIndex = randomIndex
        element.classList.add(parallax_types[randomIndex])
        i++
      });
    }
  } 
  getRandomInt(max: number) {
    return Math.floor(Math.random() * max);
  }
  onInitFunctionCall(){
    this.ngOnInit()
  }
  openImage(i:number){
    for(let j = 0; j < i; j++){
      let element = document.getElementById('imageCard'+j)
      element?.classList.remove('animate__fadeInUp')
      element?.classList.add('animate__fadeOutUpBig')
      setTimeout(function(){element!.style.display="none"},1700)
    }
    for(let k = i+1; k < document.getElementsByClassName('imageCard').length;k++){
      let element = document.getElementById('imageCard'+k)
      element?.classList.remove('animate__fadeInUp')
      element?.classList.add('animate__fadeOutDownBig')
      setTimeout(function(){element!.style.display="none"},1700)
      
    }
    let element = document.getElementById('imageCard'+i)
    element?.classList.remove('animate__fadeInUp')
    setTimeout(function(){(element?.classList.add('animate__pulse'))},100)
    setTimeout(function(){(element?.classList.add('animate__fadeOutLeftBig'))},1000)
    setTimeout(function(){element!.style.display="none"},1600)
     
    let article = document.getElementById('article')
    
    setTimeout(function(){article!.style.display = "grid"},1600)
    setTimeout(function(){article?.classList.add('animate__fadeInRightBig')},1600)

    this.current_article = i    
  }
}
