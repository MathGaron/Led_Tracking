function myslider(img)
hplot = imshow(img>1);
h = uicontrol('style','slider','units','pixel','position',[20 20 300 20]);
htext = uicontrol('style','text')
set(htext,'String',cat(2,'Minimum corr coeficient : ',int2str(1)),'position',[400 20 300 20])
addlistener(h,'ActionEvent',@(hObject, event) makeplot(hObject, event,img,hplot,htext));
function makeplot(hObject,event,img,hplot,htext)
n = get(hObject,'Value');
set(htext,'String',cat(2,'Minimum corr coeficient : ',int2str((1000*n)+1)));
set(hplot,'CData',img>((1000*n)+1));
drawnow;