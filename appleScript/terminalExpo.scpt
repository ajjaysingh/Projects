FasdUAS 1.101.10   ��   ��    k             l     ����  I    ��  	
�� .sysonotfnull��� ��� TEXT  m      
 
 �   " E n c o d i n g   c o m p l e t e 	 �� ��
�� 
subt  m       �   H T h e   e n c o d e d   f i l e s   a r e   i n   t h e   f o l d e r  ��  ��  ��        l     ��������  ��  ��        l     ��������  ��  ��        l      ��  ��    t nrepeat	display notification "Hello, world" with title "Hello" subtitle "world"	delay 6end repeatdisplay      �   �  r e p e a t  	 d i s p l a y   n o t i f i c a t i o n   " H e l l o ,   w o r l d "   w i t h   t i t l e   " H e l l o "   s u b t i t l e   " w o r l d "  	 d e l a y   6  e n d   r e p e a t  d i s p l a y         l     ��  ��    4 .notification "Hello, world!" sound name "Ping"     �   \ n o t i f i c a t i o n   " H e l l o ,   w o r l d ! "   s o u n d   n a m e   " P i n g "      l     ��������  ��  ��         l     ��������  ��  ��      ! " ! l      �� # $��   #��
ls /System/Library/Sounds
Basso.aiff     -- good, but error-like (low keys on keyboard)
Blow.aiff      -- good
Bottle.aiff    -- too short
Frog.aiff      -- chirp
Funk.aiff      -- thud
Glass.aiff     -- good (like the end of a timer)
Hero.aiff      -- good
Morse.aiff     -- 'pop'
Ping.aiff      -- good
Pop.aiff       -- shorter 'pop'
Purr.aiff      -- good
Sosumi.aiff    -- good
Submarine.aiff -- good
Tink.aiff      -- too quiet    $ � % %h 
 l s   / S y s t e m / L i b r a r y / S o u n d s  
 B a s s o . a i f f           - -   g o o d ,   b u t   e r r o r - l i k e   ( l o w   k e y s   o n   k e y b o a r d ) 
 B l o w . a i f f             - -   g o o d 
 B o t t l e . a i f f         - -   t o o   s h o r t 
 F r o g . a i f f             - -   c h i r p 
 F u n k . a i f f             - -   t h u d 
 G l a s s . a i f f           - -   g o o d   ( l i k e   t h e   e n d   o f   a   t i m e r ) 
 H e r o . a i f f             - -   g o o d 
 M o r s e . a i f f           - -   ' p o p ' 
 P i n g . a i f f             - -   g o o d 
 P o p . a i f f               - -   s h o r t e r   ' p o p ' 
 P u r r . a i f f             - -   g o o d 
 S o s u m i . a i f f         - -   g o o d 
 S u b m a r i n e . a i f f   - -   g o o d 
 T i n k . a i f f             - -   t o o   q u i e t  "  & ' & l     ��������  ��  ��   '  ( ) ( l     ��������  ��  ��   )  * + * l     ��������  ��  ��   +  , - , l      �� . /��   . � �set firstNumber to 3set secondNumber to 2set answer to (firstNumber + secondNumber + 1)set theString to "3 + 2 + 1 = "tell application "Finder"	display dialog theString & answerend tell    / � 0 0�  s e t   f i r s t N u m b e r   t o   3  s e t   s e c o n d N u m b e r   t o   2  s e t   a n s w e r   t o   ( f i r s t N u m b e r   +   s e c o n d N u m b e r   +   1 )  s e t   t h e S t r i n g   t o   " 3   +   2   +   1   =   "  t e l l   a p p l i c a t i o n   " F i n d e r "  	 d i s p l a y   d i a l o g   t h e S t r i n g   &   a n s w e r  e n d   t e l l  -  1 2 1 l     ��������  ��  ��   2  3 4 3 l     ��������  ��  ��   4  5 6 5 l     ��������  ��  ��   6  7 8 7 l     ��������  ��  ��   8  9 : 9 l      �� ; <��   ; d ^set theString to "Hello World!"tell application "Finder"	display dialog theStringend tell    < � = = �  s e t   t h e S t r i n g   t o   " H e l l o   W o r l d ! "  t e l l   a p p l i c a t i o n   " F i n d e r "  	 d i s p l a y   d i a l o g   t h e S t r i n g  e n d   t e l l  :  > ? > l     ��������  ��  ��   ?  @ A @ l     ��������  ��  ��   A  B C B l     ��������  ��  ��   C  D E D l     ��������  ��  ��   E  F G F l     ��������  ��  ��   G  H I H l      �� J K��   J I Ctell application "Finder"	display dialog "Hello world"end tell
    K � L L �  t e l l   a p p l i c a t i o n   " F i n d e r "  	 d i s p l a y   d i a l o g   " H e l l o   w o r l d "  e n d   t e l l  
 I  M N M l     ��������  ��  ��   N  O P O l     ��������  ��  ��   P  Q R Q l     ��������  ��  ��   R  S T S l     �� U V��   U  a    V � W W  a T  X Y X l     ��������  ��  ��   Y  Z [ Z l      �� \ ]��   \ � �set folderName to "scriptExper"set folderLocation to desktoptell application "Finder"	make new folder with properties {name:folderName, loaction:folderLocation}end tell    ] � ^ ^^  s e t   f o l d e r N a m e   t o   " s c r i p t E x p e r "  s e t   f o l d e r L o c a t i o n   t o   d e s k t o p   t e l l   a p p l i c a t i o n   " F i n d e r "  	 m a k e   n e w   f o l d e r   w i t h   p r o p e r t i e s   { n a m e : f o l d e r N a m e ,   l o a c t i o n : f o l d e r L o c a t i o n }  e n d   t e l l  [  _ ` _ l     ��������  ��  ��   `  a b a l     ��������  ��  ��   b  c d c l      �� e f��   e��
tell application "iTunes" to stop
tell application "iTunes" to pause/play
tell application "iTunes" to play the last track of the first library playlist
tell application "iTunes"	tell the first library playlist		get the artist of the last track	end tellend tell
tell application "iTunes" to get the name of the last track of the first library playlisttell application "iTunes"	tell the first library playlist		get the duration of the last track	end tellend tell    f � g g� 
 t e l l   a p p l i c a t i o n   " i T u n e s "   t o   s t o p 
 t e l l   a p p l i c a t i o n   " i T u n e s "   t o   p a u s e / p l a y 
 t e l l   a p p l i c a t i o n   " i T u n e s "   t o   p l a y   t h e   l a s t   t r a c k   o f   t h e   f i r s t   l i b r a r y   p l a y l i s t 
  t e l l   a p p l i c a t i o n   " i T u n e s "  	 t e l l   t h e   f i r s t   l i b r a r y   p l a y l i s t  	 	 g e t   t h e   a r t i s t   o f   t h e   l a s t   t r a c k  	 e n d   t e l l  e n d   t e l l 
  t e l l   a p p l i c a t i o n   " i T u n e s "   t o   g e t   t h e   n a m e   o f   t h e   l a s t   t r a c k   o f   t h e   f i r s t   l i b r a r y   p l a y l i s t  t e l l   a p p l i c a t i o n   " i T u n e s "  	 t e l l   t h e   f i r s t   l i b r a r y   p l a y l i s t  	 	 g e t   t h e   d u r a t i o n   o f   t h e   l a s t   t r a c k  	 e n d   t e l l  e n d   t e l l  d  h i h l     ��������  ��  ��   i  j k j l     ��������  ��  ��   k  l m l l      �� n o��   ntell application "Safari" to close every windowtell application "Safari" to open location "http://automator.us"tell application "Safari" to get the position of the front windowtell application "Safari" to get the bounds of window 1tell application "Safari" to set the bounds of the front window to {0, 22, 800, 1024}tell application "Finder" to get the bounds of the window of the desktoptell application "Safari" to set the bounds of the front window to �	{0, 22, (3rd item of the result), (4th item of the result)}    o � p p  t e l l   a p p l i c a t i o n   " S a f a r i "   t o   c l o s e   e v e r y   w i n d o w  t e l l   a p p l i c a t i o n   " S a f a r i "   t o   o p e n   l o c a t i o n   " h t t p : / / a u t o m a t o r . u s "  t e l l   a p p l i c a t i o n   " S a f a r i "   t o   g e t   t h e   p o s i t i o n   o f   t h e   f r o n t   w i n d o w  t e l l   a p p l i c a t i o n   " S a f a r i "   t o   g e t   t h e   b o u n d s   o f   w i n d o w   1  t e l l   a p p l i c a t i o n   " S a f a r i "   t o   s e t   t h e   b o u n d s   o f   t h e   f r o n t   w i n d o w   t o   { 0 ,   2 2 ,   8 0 0 ,   1 0 2 4 }  t e l l   a p p l i c a t i o n   " F i n d e r "   t o   g e t   t h e   b o u n d s   o f   t h e   w i n d o w   o f   t h e   d e s k t o p  t e l l   a p p l i c a t i o n   " S a f a r i "   t o   s e t   t h e   b o u n d s   o f   t h e   f r o n t   w i n d o w   t o   �  	 { 0 ,   2 2 ,   ( 3 r d   i t e m   o f   t h e   r e s u l t ) ,   ( 4 t h   i t e m   o f   t h e   r e s u l t ) }  m  q r q l     ��������  ��  ��   r  s t s l     ��������  ��  ��   t  u v u l      �� w x��   w��tell application "Finder"	close every window	open home	tell the front Finder window		set toolbar visible to true		set the sidebar width to 135		set the current view to column view		set the bounds to {36, 116, 511, 674}	end tell	open folder "Documents" of home	tell the front Finder window		set toolbar visible to false		set the current view to flow view		set the bounds to {528, 116, 1016, 674}	end tell	select the last Finder windowend tell    x � y y�  t e l l   a p p l i c a t i o n   " F i n d e r "  	 c l o s e   e v e r y   w i n d o w  	 o p e n   h o m e  	 t e l l   t h e   f r o n t   F i n d e r   w i n d o w  	 	 s e t   t o o l b a r   v i s i b l e   t o   t r u e  	 	 s e t   t h e   s i d e b a r   w i d t h   t o   1 3 5  	 	 s e t   t h e   c u r r e n t   v i e w   t o   c o l u m n   v i e w  	 	 s e t   t h e   b o u n d s   t o   { 3 6 ,   1 1 6 ,   5 1 1 ,   6 7 4 }  	 e n d   t e l l  	 o p e n   f o l d e r   " D o c u m e n t s "   o f   h o m e  	 t e l l   t h e   f r o n t   F i n d e r   w i n d o w  	 	 s e t   t o o l b a r   v i s i b l e   t o   f a l s e  	 	 s e t   t h e   c u r r e n t   v i e w   t o   f l o w   v i e w  	 	 s e t   t h e   b o u n d s   t o   { 5 2 8 ,   1 1 6 ,   1 0 1 6 ,   6 7 4 }  	 e n d   t e l l  	 s e l e c t   t h e   l a s t   F i n d e r   w i n d o w  e n d   t e l l  v  z { z l     ��������  ��  ��   {  | } | l     ��������  ��  ��   }  ~  ~ l      �� � ���   ���tell application "Finder" to close every windowtell application "Finder" to open hometell application "Finder" to set toolbar visible of the front Finder window to truetell application "Finder" to set the sidebar width of the front Finder window to 135tell application "Finder" to set the current view of the front Finder window to column viewtell application "Finder" to set the bounds of the front Finder window to {36, 116, 511, 674}tell application "Finder" to open folder "Documents" of hometell application "Finder" to set toolbar visible of the front Finder window to falsetell application "Finder" to set statusbar visible of the front Finder window to truetell application "Finder" to set the current view of the front Finder window to flow viewtell application "Finder" to set the bounds of the front Finder window to {528, 116, 1016, 674}tell application "Finder" to select the last Finder window
		
		OR
tell application "Finder"
  close every window
  open home
  set the current view of the front Finder window to column view
  open folder "Desktop" of home
  set the current view of the front Finder window to icon view
  select last finder window
end tell
    � � � �	B  t e l l   a p p l i c a t i o n   " F i n d e r "   t o   c l o s e   e v e r y   w i n d o w  t e l l   a p p l i c a t i o n   " F i n d e r "   t o   o p e n   h o m e  t e l l   a p p l i c a t i o n   " F i n d e r "   t o   s e t   t o o l b a r   v i s i b l e   o f   t h e   f r o n t   F i n d e r   w i n d o w   t o   t r u e  t e l l   a p p l i c a t i o n   " F i n d e r "   t o   s e t   t h e   s i d e b a r   w i d t h   o f   t h e   f r o n t   F i n d e r   w i n d o w   t o   1 3 5  t e l l   a p p l i c a t i o n   " F i n d e r "   t o   s e t   t h e   c u r r e n t   v i e w   o f   t h e   f r o n t   F i n d e r   w i n d o w   t o   c o l u m n   v i e w  t e l l   a p p l i c a t i o n   " F i n d e r "   t o   s e t   t h e   b o u n d s   o f   t h e   f r o n t   F i n d e r   w i n d o w   t o   { 3 6 ,   1 1 6 ,   5 1 1 ,   6 7 4 }  t e l l   a p p l i c a t i o n   " F i n d e r "   t o   o p e n   f o l d e r   " D o c u m e n t s "   o f   h o m e  t e l l   a p p l i c a t i o n   " F i n d e r "   t o   s e t   t o o l b a r   v i s i b l e   o f   t h e   f r o n t   F i n d e r   w i n d o w   t o   f a l s e  t e l l   a p p l i c a t i o n   " F i n d e r "   t o   s e t   s t a t u s b a r   v i s i b l e   o f   t h e   f r o n t   F i n d e r   w i n d o w   t o   t r u e  t e l l   a p p l i c a t i o n   " F i n d e r "   t o   s e t   t h e   c u r r e n t   v i e w   o f   t h e   f r o n t   F i n d e r   w i n d o w   t o   f l o w   v i e w  t e l l   a p p l i c a t i o n   " F i n d e r "   t o   s e t   t h e   b o u n d s   o f   t h e   f r o n t   F i n d e r   w i n d o w   t o   { 5 2 8 ,   1 1 6 ,   1 0 1 6 ,   6 7 4 }  t e l l   a p p l i c a t i o n   " F i n d e r "   t o   s e l e c t   t h e   l a s t   F i n d e r   w i n d o w  
 	 	 
 	 	 O R 
 t e l l   a p p l i c a t i o n   " F i n d e r " 
     c l o s e   e v e r y   w i n d o w 
     o p e n   h o m e 
     s e t   t h e   c u r r e n t   v i e w   o f   t h e   f r o n t   F i n d e r   w i n d o w   t o   c o l u m n   v i e w 
     o p e n   f o l d e r   " D e s k t o p "   o f   h o m e 
     s e t   t h e   c u r r e n t   v i e w   o f   t h e   f r o n t   F i n d e r   w i n d o w   t o   i c o n   v i e w 
     s e l e c t   l a s t   f i n d e r   w i n d o w 
 e n d   t e l l 
   � � � l     ��������  ��  ��   �  � � � l     ��������  ��  ��   �  � � � l      �� � ���   ���
get: used to access the current values of a window property
set: used to apply a new value to a window property
open: causes a window to display in the Finder
close: causes a window to close


tell application "Finder" to select the last Finder window

tell application "Finder" to get the bounds of the desktop
tell application "Finder" to get the bounds of the front Finder windowtell application "Finder" to set the bounds of the front Finder window to {24, 96, 524, 396}

tell application "Finder" to get the position of the front Finder windowtell application "Finder" to set the position of the front Finder window to {90, 134}

tell application "Finder" to �
 set the current view of the front Finder window to list view / flow view / column view / icon view
tell application "Finder" to �
 get the current view of the front Finder window

tell application "Finder" to set the sidebar width of �
 Finder window 1 to the sidebar width of Finder window 2
tell application "Finder" to set the sidebar width of  every Finder window to 0
tell application "Finder" to set the sidebar width of  Finder window 1 to 240

tell application "Finder" to set statusbar visible of  Finder window 1 to true

tell application "Finder" to set toolbar visible of  Finder window 1 to false
tell application "Finder" to set toolbar visible of  Finder window 1 to true

tell application "Finder" to  set toolbar visible of the front Finder window to false
tell application "Finder" to  set toolbar visible of the front Finder window to true
tell application "Finder" to set target of �	the front Finder window to �	folder "lab" of folder "Projects" of folder "chaser" of �	folder "Users" of disk "Macintosh HD"    � � � �N 
 g e t :   u s e d   t o   a c c e s s   t h e   c u r r e n t   v a l u e s   o f   a   w i n d o w   p r o p e r t y 
 s e t :   u s e d   t o   a p p l y   a   n e w   v a l u e   t o   a   w i n d o w   p r o p e r t y 
 o p e n :   c a u s e s   a   w i n d o w   t o   d i s p l a y   i n   t h e   F i n d e r 
 c l o s e :   c a u s e s   a   w i n d o w   t o   c l o s e 
 
 
 t e l l   a p p l i c a t i o n   " F i n d e r "   t o   s e l e c t   t h e   l a s t   F i n d e r   w i n d o w 
 
 t e l l   a p p l i c a t i o n   " F i n d e r "   t o   g e t   t h e   b o u n d s   o f   t h e   d e s k t o p 
 t e l l   a p p l i c a t i o n   " F i n d e r "   t o   g e t   t h e   b o u n d s   o f   t h e   f r o n t   F i n d e r   w i n d o w  t e l l   a p p l i c a t i o n   " F i n d e r "   t o   s e t   t h e   b o u n d s   o f   t h e   f r o n t   F i n d e r   w i n d o w   t o   { 2 4 ,   9 6 ,   5 2 4 ,   3 9 6 } 
 
 t e l l   a p p l i c a t i o n   " F i n d e r "   t o   g e t   t h e   p o s i t i o n   o f   t h e   f r o n t   F i n d e r   w i n d o w  t e l l   a p p l i c a t i o n   " F i n d e r "   t o   s e t   t h e   p o s i t i o n   o f   t h e   f r o n t   F i n d e r   w i n d o w   t o   { 9 0 ,   1 3 4 } 
 
 t e l l   a p p l i c a t i o n   " F i n d e r "   t o   � 
   s e t   t h e   c u r r e n t   v i e w   o f   t h e   f r o n t   F i n d e r   w i n d o w   t o   l i s t   v i e w   /   f l o w   v i e w   /   c o l u m n   v i e w   /   i c o n   v i e w 
 t e l l   a p p l i c a t i o n   " F i n d e r "   t o   � 
   g e t   t h e   c u r r e n t   v i e w   o f   t h e   f r o n t   F i n d e r   w i n d o w 
 
 t e l l   a p p l i c a t i o n   " F i n d e r "   t o   s e t   t h e   s i d e b a r   w i d t h   o f   � 
   F i n d e r   w i n d o w   1   t o   t h e   s i d e b a r   w i d t h   o f   F i n d e r   w i n d o w   2 
 t e l l   a p p l i c a t i o n   " F i n d e r "   t o   s e t   t h e   s i d e b a r   w i d t h   o f     e v e r y   F i n d e r   w i n d o w   t o   0 
 t e l l   a p p l i c a t i o n   " F i n d e r "   t o   s e t   t h e   s i d e b a r   w i d t h   o f     F i n d e r   w i n d o w   1   t o   2 4 0 
 
 t e l l   a p p l i c a t i o n   " F i n d e r "   t o   s e t   s t a t u s b a r   v i s i b l e   o f     F i n d e r   w i n d o w   1   t o   t r u e 
 
 t e l l   a p p l i c a t i o n   " F i n d e r "   t o   s e t   t o o l b a r   v i s i b l e   o f     F i n d e r   w i n d o w   1   t o   f a l s e 
 t e l l   a p p l i c a t i o n   " F i n d e r "   t o   s e t   t o o l b a r   v i s i b l e   o f     F i n d e r   w i n d o w   1   t o   t r u e 
 
 t e l l   a p p l i c a t i o n   " F i n d e r "   t o     s e t   t o o l b a r   v i s i b l e   o f   t h e   f r o n t   F i n d e r   w i n d o w   t o   f a l s e 
 t e l l   a p p l i c a t i o n   " F i n d e r "   t o     s e t   t o o l b a r   v i s i b l e   o f   t h e   f r o n t   F i n d e r   w i n d o w   t o   t r u e 
  t e l l   a p p l i c a t i o n   " F i n d e r "   t o   s e t   t a r g e t   o f   �  	 t h e   f r o n t   F i n d e r   w i n d o w   t o   �  	 f o l d e r   " l a b "   o f   f o l d e r   " P r o j e c t s "   o f   f o l d e r   " c h a s e r "   o f   �  	 f o l d e r   " U s e r s "   o f   d i s k   " M a c i n t o s h   H D "  �  � � � l     ��������  ��  ��   �  � � � l      �� � ���   � � �tell application "Finder" to �	set the target of the front Finder window to the startup disktell application "Finder" to get the target of the front window    � � � �>  t e l l   a p p l i c a t i o n   " F i n d e r "   t o   �  	 s e t   t h e   t a r g e t   o f   t h e   f r o n t   F i n d e r   w i n d o w   t o   t h e   s t a r t u p   d i s k  t e l l   a p p l i c a t i o n   " F i n d e r "   t o   g e t   t h e   t a r g e t   o f   t h e   f r o n t   w i n d o w  �  � � � l     ��������  ��  ��   �  � � � l      �� � ���   � G Atell application "Finder" to get the target of the front window    � � � � �  t e l l   a p p l i c a t i o n   " F i n d e r "   t o   g e t   t h e   t a r g e t   o f   t h e   f r o n t   w i n d o w  �  � � � l     ��������  ��  ��   �  � � � l      �� � ���   �c]tell application "Finder" to get the index of the front Finder windowtell application "Finder" to get the index of the back Finder windowtell application "Finder" to get the index of the last Finder windowtell application "Finder" to get the index of the Finder window before the last Finder windowtell application "Finder" to get the index of the Finder window after the first Finder window
  by name:
	Finder window "Documents"
	by numeric index:
	Finder window 1
  by descriptive index:
	the first Finder window
	the second Finder window
	the fifth Finder window
	the 1st Finder window
	the 23rd Finder window
  by relative position index:
	the front Finder window
	the middle Finder window
	the back Finder window
	the last Finder window
  by random index:
	some Finder window

tell application "Finder" to set the index of the last Finder window to 1    � � � ��  t e l l   a p p l i c a t i o n   " F i n d e r "   t o   g e t   t h e   i n d e x   o f   t h e   f r o n t   F i n d e r   w i n d o w  t e l l   a p p l i c a t i o n   " F i n d e r "   t o   g e t   t h e   i n d e x   o f   t h e   b a c k   F i n d e r   w i n d o w  t e l l   a p p l i c a t i o n   " F i n d e r "   t o   g e t   t h e   i n d e x   o f   t h e   l a s t   F i n d e r   w i n d o w  t e l l   a p p l i c a t i o n   " F i n d e r "   t o   g e t   t h e   i n d e x   o f   t h e   F i n d e r   w i n d o w   b e f o r e   t h e   l a s t   F i n d e r   w i n d o w  t e l l   a p p l i c a t i o n   " F i n d e r "   t o   g e t   t h e   i n d e x   o f   t h e   F i n d e r   w i n d o w   a f t e r   t h e   f i r s t   F i n d e r   w i n d o w 
     b y   n a m e : 
 	 F i n d e r   w i n d o w   " D o c u m e n t s " 
 	 b y   n u m e r i c   i n d e x : 
 	 F i n d e r   w i n d o w   1 
     b y   d e s c r i p t i v e   i n d e x : 
 	 t h e   f i r s t   F i n d e r   w i n d o w 
 	 t h e   s e c o n d   F i n d e r   w i n d o w 
 	 t h e   f i f t h   F i n d e r   w i n d o w 
 	 t h e   1 s t   F i n d e r   w i n d o w 
 	 t h e   2 3 r d   F i n d e r   w i n d o w 
     b y   r e l a t i v e   p o s i t i o n   i n d e x : 
 	 t h e   f r o n t   F i n d e r   w i n d o w 
 	 t h e   m i d d l e   F i n d e r   w i n d o w 
 	 t h e   b a c k   F i n d e r   w i n d o w 
 	 t h e   l a s t   F i n d e r   w i n d o w 
     b y   r a n d o m   i n d e x : 
 	 s o m e   F i n d e r   w i n d o w 
 
 t e l l   a p p l i c a t i o n   " F i n d e r "   t o   s e t   t h e   i n d e x   o f   t h e   l a s t   F i n d e r   w i n d o w   t o   1  �  � � � l     ��������  ��  ��   �  � � � l      �� � ���   �tell application "Finder" to get the index of the first Finder windowtell application "Finder" to get the index of the second Finder windowtell application "Finder" to get the index of the 1st Finder windowtell application "Finder" to get the index of the 2nd Finder window    � � � �,  t e l l   a p p l i c a t i o n   " F i n d e r "   t o   g e t   t h e   i n d e x   o f   t h e   f i r s t   F i n d e r   w i n d o w  t e l l   a p p l i c a t i o n   " F i n d e r "   t o   g e t   t h e   i n d e x   o f   t h e   s e c o n d   F i n d e r   w i n d o w  t e l l   a p p l i c a t i o n   " F i n d e r "   t o   g e t   t h e   i n d e x   o f   t h e   1 s t   F i n d e r   w i n d o w  t e l l   a p p l i c a t i o n   " F i n d e r "   t o   g e t   t h e   i n d e x   o f   t h e   2 n d   F i n d e r   w i n d o w  �  � � � l     ��������  ��  ��   �  � � � l      � � ��   �"tell application "Finder" to open startup disktell application "Finder" to open hometell application "Finder" to get the index of Finder window "Macintosh HD"tell application "Finder" to get the name of Finder window 1tell application "Finder" to get the name of Finder window 2    � � � �8  t e l l   a p p l i c a t i o n   " F i n d e r "   t o   o p e n   s t a r t u p   d i s k  t e l l   a p p l i c a t i o n   " F i n d e r "   t o   o p e n   h o m e  t e l l   a p p l i c a t i o n   " F i n d e r "   t o   g e t   t h e   i n d e x   o f   F i n d e r   w i n d o w   " M a c i n t o s h   H D "  t e l l   a p p l i c a t i o n   " F i n d e r "   t o   g e t   t h e   n a m e   o f   F i n d e r   w i n d o w   1  t e l l   a p p l i c a t i o n   " F i n d e r "   t o   g e t   t h e   n a m e   o f   F i n d e r   w i n d o w   2  �  � � � l     �~�}�|�~  �}  �|   �  � � � l      �{ � ��{   �=7
tell application "Finder" to open home
tell application "Finder" to close Finder window "F"
tell application "Finder" to get name of front Finder window
tell application "Finder" to open startup disk
tell application "Finder" to  get the index of Finder window "Macintosh HD"tell application "iTunes" to play    � � � �n 
 t e l l   a p p l i c a t i o n   " F i n d e r "   t o   o p e n   h o m e 
 t e l l   a p p l i c a t i o n   " F i n d e r "   t o   c l o s e   F i n d e r   w i n d o w   " F " 
 t e l l   a p p l i c a t i o n   " F i n d e r "   t o   g e t   n a m e   o f   f r o n t   F i n d e r   w i n d o w 
 t e l l   a p p l i c a t i o n   " F i n d e r "   t o   o p e n   s t a r t u p   d i s k 
 t e l l   a p p l i c a t i o n   " F i n d e r "   t o     g e t   t h e   i n d e x   o f   F i n d e r   w i n d o w   " M a c i n t o s h   H D "  t e l l   a p p l i c a t i o n   " i T u n e s "   t o   p l a y  �  � � � l     �z�y�x�z  �y  �x   �  � � � l     �w�v�u�w  �v  �u   �  � � � l      �t � ��t   � I Ctell application "Terminal"	do script "alter.py accord"end tell    � � � � �  t e l l   a p p l i c a t i o n   " T e r m i n a l "  	 d o   s c r i p t   " a l t e r . p y   a c c o r d "  e n d   t e l l  �  ��s � l     �r�q�p�r  �q  �p  �s       �o � ��o   � �n
�n .aevtoappnull  �   � **** � �m ��l�k � ��j
�m .aevtoappnull  �   � **** � k      � �  �i�i  �l  �k   �   �  
�h �g
�h 
subt
�g .sysonotfnull��� ��� TEXT�j ���l ascr  ��ޭ