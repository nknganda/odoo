from openerp import models, fields, api, _
from openerp.exceptions import except_orm, Warning, RedirectWarning, ValidationError
from openerp import api, tools, SUPERUSER_ID

class product_images(models.Model):
	_name = "product.images"
	_description = "Additional Product Images"
	_order = "sequence"

	@api.model
	def _default_seq(self):
	   return int(self.env['product.images'].search([], order="id desc", limit=1).id) + 1

	sequence = fields.Integer('Sequence', required=True, default=_default_seq)
	product_id = fields.Many2one('product.template', 'Product', required=True)
	name = fields.Char('Image Name', size=160, help="This image name will appear when mouse hovers around the image")
	publish = fields.Boolean('Publish on Website', default=True,  help="This image will be available on website if this box is checked")
	image = fields.Binary("Image", attachment=True, required=True,
        	help="This field holds the image used as image for the product, limited to 1024x1024px.")
    	image_medium = fields.Binary("Medium-sized image", required=True,
        	compute='_compute_images', inverse='_inverse_image_medium', store=True, attachment=True,
        	help="Medium-sized image of the product. It is automatically "\
             "resized as a 128x128px image, with aspect ratio preserved, "\
             "only when the image exceeds one of those sizes. Use this field in form views or some kanban views.")
    	image_small = fields.Binary("Small-sized image",
        	compute='_compute_images', inverse='_inverse_image_small', store=True, attachment=True, required=True,
        	help="Small-sized image of the product. It is automatically "\
             "resized as a 64x64px image, with aspect ratio preserved. "\
             "Use this field anywhere a small image is required.")

 	_sql_constraints = [
    		('sequence_unique', 'unique(sequence)', 'Sequence Number already exists!')
	] 

	@api.depends('image')
    	def _compute_images(self):
            for rec in self:
            	rec.image_medium = tools.image_resize_image_medium(rec.image, avoid_if_small=True)
            	rec.image_small = tools.image_resize_image_small(rec.image)

    	def _inverse_image_medium(self):
            for rec in self:
            	rec.image = tools.image_resize_image_big(rec.image_medium)

    	def _inverse_image_small(self):
            for rec in self:
           	rec.image = tools.image_resize_image_big(rec.image_small)

class product_template(models.Model):
	_name = "product.template"
	_inherit = ['product.template']

	cursors = ["auto","crosshair","default","e-resize","grab","help","move","n-resize","ne-resize","nw-resize","pointer",
		"progress","s-resize","se-resize","sw-resize","text","w-resize","wait","not-allowed","no-drop"]
	zoomTypes = ["window","lens","inner"]
	lensShapes = ["round","square"]
	image_ids = fields.One2many('product.images', 'product_id', 'Additional Images')
	scrollZoom = fields.Boolean('Mousewheel Zoom', default=True, help="Activate or deactivate the mousewheel zooming in and out")
	easing = fields.Boolean('Zoom Easing', default=True, help="This determines how slowly the zoomed image is moved and displayed on"\
	" the window. only affect window type of zoom")
	tint = fields.Boolean('Tint Image', default=False, help="You can easily set tints for the zoom, you can set the colour and opacity of the"\
								" tint to be any value")
	tintColour = fields.Char('Tint Color', size=4, default="#F90", help="Enter HTML color code only. e.g #333")
	tintOpacity = fields.Float('Tint Opacity', digits=(1,1), default=0.4, help="Enter Value between 0 and 1 only; default is 0.4")
	lensShape = fields.Selection(
			[
				(ls, ls) for ls in lensShapes
			], 
			'Lens Shape', default="round", required=True,
			help="Choose between 'round' and 'square' lens shape for your 'lens' zoom option; default is 'round'")
	zoomType = fields.Selection(
			[
				(zm, zm) for zm in zoomTypes
			], 
			'Zoom Type', default="window", required=True,
			help="There are several Zoom options to choose from. This affect how your image is magnified to the viewer; default is 'window'")
	lensFadeOut = fields.Selection(
			[
				(lfo, lfo) for lfo in range (10,1001)  
			], 
			'Lens Fade Out (ms)', default=10, required=True,
			help="The Lens Fade Out time; default is 10ms")
	lensFadeIn = fields.Selection(
			[
				(lfi, lfi) for lfi in range (10,1001)  
			], 
			'Lens Fade In (ms)', default=10, required=True,
			help="The Lens Fade In time; default is 10ms")
	zoomWindowFadeOut = fields.Selection(
			[
				(fo, fo) for fo in range (10,1001)  
			], 
			'Zoom Window Fade Out (ms)', default=10, required=True,
			help="The Zoom Window Fade out time; default is 10ms")
	zoomWindowFadeIn = fields.Selection(
			[
				(fi, fi) for fi in range (10,1001)  
			], 
			'Zoom Window Fade In (ms)', default=10, required=True,
			help="The Zoom Window Fade in time; default is 10ms")
	zoomWindowHeight = fields.Selection(
			[
				(zh, zh) for zh in range (100,1025)  
			], 
			'Zoom Window Height (px)', default=400, required=True,
			help="The Zoom Window Height in Pixels; default is 400px")
	zoomWindowWidth = fields.Selection(
			[
				(zw, zw) for zw in range (100,1025)  
			], 
			'Zoom Window Width (px)', default=400, required=True,
			help="The Zoom Window Width in Pixels; default is 400px")
	lensSize = fields.Selection(
			[
				(lz, lz) for lz in range (100,401)  
			], 
			'Lens Size (px)', default=300, required=True,
			help="The Lens dimension; diameter for round lens or width for square lens; default is 300px")
	zoomWindowPosition = fields.Selection(
			[
				(value, value) for value in range (1,13)  
			], 
			'Zoom Window Position', default=1, required=True,
			help="The Zoom Window Position can be positioned in 12 different locations outside the product image; default is 1")
	cursor = fields.Selection(
			[
				(cur, cur) for cur in cursors  
			], 
			'Cursor Type', default="default", required=True,
			help="Choose the type of cursor to use when zooming the image")
