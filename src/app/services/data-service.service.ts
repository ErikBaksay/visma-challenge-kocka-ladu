import { Injectable } from '@angular/core';
import { HttpClient} from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class DataServiceService {
  private data:any = []

  constructor(private http : HttpClient) {}

  getData(){
    const url ='http://10.0.5.151/api/get/newcomers'
    return this.http.get(url)
  }

}
