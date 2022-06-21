import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';
import { FormType } from 'src/app/base-class/base-form';

@Injectable({
  providedIn: 'root'
})
export class EventManagerService {
  
  private switchFormSource = new Subject<any>();
  switchFormEvent = this.switchFormSource.asObservable();
  switchFormEmit(formType: FormType) {
    this.switchFormSource.next(formType)
  }
  
  private closeFormSource = new Subject<any>();
  closeFormEvent = this.closeFormSource.asObservable();
  closeFormEmit() {
    this.closeFormSource.next(1)
  }
  
  private userChangedSource = new Subject<any>();
  userChangedEvent = this.userChangedSource.asObservable();
  userChangedEmit() {
    this.userChangedSource.next(1)
  }
  
  private openMenuSource = new Subject<any>();
  openMenuEvent = this.openMenuSource.asObservable();
  openMenuEmit() {
    this.openMenuSource.next(1)
  }
  
  private userRoleChangeSource = new Subject<any>();
  userRoleChangeEvent = this.userRoleChangeSource.asObservable();
  userRoleChangeEmit() {
    this.userRoleChangeSource.next(1)
  }
  
  private statUpdateSource = new Subject<any>();
  statUpdateEvent = this.statUpdateSource.asObservable();
  statUpdateEmit() {
    this.statUpdateSource.next(1)
  }
  
  private newsDeleteSource = new Subject<any>();
  newsDeleteEvent = this.newsDeleteSource.asObservable();
  newsDeleteEmit() {
    this.newsDeleteSource.next(1)
  }
}
