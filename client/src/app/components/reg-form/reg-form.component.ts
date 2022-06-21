import { Component, ElementRef, EventEmitter, OnInit, Output, ViewChild } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { BaseForm } from 'src/app/base-class/base-form';
import { AuthService } from 'src/app/services/auth/auth.service';
import { EventManagerService } from 'src/app/services/event-manager/event-manager.service';

@Component({
  selector: 'app-reg-form',
  templateUrl: './reg-form.component.html',
  styleUrls: ['./reg-form.component.scss']
})
export class RegFormComponent extends BaseForm implements OnInit {
  
  regForm = this.formBuilder.group({
    mail: '',
    login: '',
    name: '',
    password: '',
    repeat_password: ''
  });
  error = false

  constructor(
    private formBuilder: FormBuilder,
    private authService: AuthService,
    eventManagerService: EventManagerService,
  ) { 
    super(eventManagerService);
  }

  ngOnInit(): void {
    this.error = false
  }
  
  onSubmit(): void {
    this.authService.registrate(
      this.regForm.value.mail,
      this.regForm.value.name,
      this.regForm.value.login,
      this.regForm.value.password,
      this.regForm.value.repeat_password
    ).subscribe( {
      next: () => {
        this.eventManagerService.userChangedEmit();
      },
      error: () => {
        this.error = true
      }
    })
  }
}
