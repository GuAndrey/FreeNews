import { Component, ElementRef, EventEmitter, Output, ViewChild } from '@angular/core';
import { EventManagerService } from '../services/event-manager/event-manager.service'

export enum FormType {
  LOGIN,
  REG,
  MENU,
} 
@Component({ template: '' })
export abstract class BaseForm {

  FormType = FormType
  @ViewChild('outer') outerElement?: ElementRef;

  constructor(protected eventManagerService: EventManagerService) {
  }
  
  switchForm(form: FormType) {
    this.eventManagerService.switchFormEmit(form);
  }
  
  close(event: Event): void {
    if (event.target == this.outerElement?.nativeElement) {
      this.eventManagerService.closeFormEmit();
    }
  }
}
