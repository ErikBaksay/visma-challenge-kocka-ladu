import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.sass']
})
export class NavbarComponent implements OnInit {

  categories = ['Newcomers', 'New Projects', 'Tournaments', 'Sport Challenges', 'Other events','Create a new post']
  routes = ['newcomers','new-projects','tournaments','sport-challenges','other-events', 'create']
  current_category = 'Newcomers'

  constructor( private router : Router) { }

  ngOnInit(): void {
  }
  menuOpen(){
    let menu = document.getElementById("collapsableMenu")
    if (menu!.style.display == "none"){
      menu!.style.display = "block"
    }else{
      menu!.style.display = "none"
    }
  }
  
  chooseCategory(i:number){
    this.current_category = this.categories[i]
    this.router.navigate([this.routes[i]])
    document.getElementById('collapsableMenu')!.style.display='none'
  }
}
