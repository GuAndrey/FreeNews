import { Component, Input, OnInit } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { ActivatedRoute } from '@angular/router';
import { Comment } from '../../services/comment/Comment';
import { CommentService } from '../../services/comment/comment.service';
import { News } from '../../services/news/News';
import { NewsService } from '../../services/news/news.service';
import { StatService } from '../../services/stat/stat.service';

@Component({
  selector: 'app-news-page',
  templateUrl: './news-page.component.html',
  styleUrls: ['./news-page.component.scss']
})
export class NewsPageComponent implements OnInit {
  news?: News
  
  commentForm = this.formBuilder.group({
    comment: '',
  });
  commentList: Comment[] = []

  constructor(
    private formBuilder: FormBuilder,
    private newsService: NewsService,
    private commentService: CommentService,
    private statService: StatService,
    private route: ActivatedRoute
    ) { }
    
  ngOnInit(): void {
    this.getNews()
    this.getComments()
  }
  
  ngDoCheck(): void {
    this.setInfoPosition()
  }
  
  ngAfterViewChecked(): void {
    this.setNewsContent();
  }
  
  setInfoPosition() {
    let container  = <HTMLElement>document.getElementsByClassName('container')[0];
    let info =  <HTMLElement>document.getElementsByClassName('info')[0];
    info.style.left = String(container.offsetLeft + container.offsetWidth + 20) + "px";
  }
  
  setNewsContent() {
    if (this.news) {
      let content = <HTMLElement>document.getElementsByClassName('news-content')[0];
      content.innerHTML = this.news.content;
      let images = <HTMLCollection>document.getElementsByTagName('img');
      for (let i = 0; i < images.length; i++) {
        let image = <HTMLElement>images.item(i);
        image.style.maxWidth = '700px'
      }
    }
  }
  
  getNews(){
    const id = Number(this.route.snapshot.paramMap.get('id'));
    this.statService.addView(id).subscribe({ 
      next: () => {
        this.newsService.getNewsById(id).subscribe(news => {
          this.news = news;
        });
      },
      error: () => {
        this.newsService.getNewsById(id).subscribe(news => {
          this.news = news;
        });
      },
    })
  }
  
  getComments(){
    const id = Number(this.route.snapshot.paramMap.get('id'));
    this.commentService.getCommentsByNewsId(id).subscribe(commentList => {
      this.commentList = commentList
    })
  }
  
  swapLike(){
    if (this.news) {
      this.statService.swapLike(this.news.id).subscribe(_ => {
        this.getNews();
      })
    }
  }
  
  swapRep(){
    if (this.news) {
      this.statService.swapRep(this.news.id).subscribe(_ => {
        this.getNews();
      })
    }
  }
  
  swapFavorite(){
    if (this.news) {
      this.statService.swapFavorite(this.news.id).subscribe(_ => {
        this.getNews();
      })
    }
  }
  
  sendComment(){
    this.getComments();
    if (this.news) {
      this.commentService.addComments(this.news.id, this.commentForm.value.comment).subscribe(_ => {
        this.getComments();
        this.commentForm.reset()
      })
    }
  }
}
