def ppt_make(filename):

	now = datetime.utcnow()
	# Using template slide, make title slide and save
	pptpath = 'template.pptx'
	prs = Presentation(pptpath)

	# Make the title slide
	title_slide_layout = prs.slide_layouts[0]
	slide = prs.slides.add_slide(title_slide_layout)
	title_name = slide.shapes.placeholders[10]
	title_loc = slide.shapes.placeholders[11]
	title = slide.shapes.placeholders[12]
	title_sub = slide.shapes.placeholders[14]
	title_name.text = 'Declan Cockburn'
	title_loc.text = '{}/{}/{}, HBO, US. Workstream'.format(now.year, now.month, now.day)
	title_sub.text = 'Auto Generated PPT on {}/{}/{} at {}:{} (UTC)'.format(now.year, now.month, now.day, now.hour, now.minute)
	title.text = 'Collector Swap Prediction Tool'
	prs.save('Collector_Swap_Prediction.pptx')
	prs.save(filename)

# Populate the rest of the content slides with data/pictures
def ppt_populate(datalist, filename):
	machines = [df.columns.values[0] for df in datalist]
	for machine in machines:
		prs = Presentation(filename)
		blank_slide_layout = prs.slide_layouts[1]
		slide = prs.slides.add_slide(blank_slide_layout)
		shapes = slide.shapes


		# Image 1 placement
		pic1_path = 'output/{}.png'.format(machine)
		left1 = Cm(1)
		top1 = Cm(3)
		height1 = Cm(10)
		pic1 = slide.shapes.add_picture(pic1_path, left1, top1, height=height1)

		# Impage2 placement
		pic2_path = 'output\\table_{}.png'.format(machine)
		top2 = Cm(1.2)
		width2 = Cm(9)
		left2 = pic1.width + Cm(1)
		pic2 = slide.shapes.add_picture(pic2_path, left2, top2, width=width2)
		# pic2.crop_bottom = 0.02
		# pic2.crop_top = 0.03
		# pic2.crop_left = 0.1
		# pic2.crop_right = 0.1
		title2 = shapes.title
		subtitle2 = shapes.placeholders[14]
		text2 = shapes.placeholders[13]
		subtitle2.text = col_swapped_dic[machine.split('.')[0]]
		text2.text = ' '
		title2.text = '{}'.format(machine.split('.')[0])
		prs.save(filename)

def ppt_summaryslide(filename):
	prs = Presentation(filename)
	blank_slide_layout = prs.slide_layouts[1]
	slide = prs.slides.add_slide(blank_slide_layout)
	shapes = slide.shapes
	title2 = shapes.title
	subtitle2 = shapes.placeholders[14]
	text2 = shapes.placeholders[13]
	subtitle2.text = 'Color-coded for swaps needed in < 5 weeks'
	text2.text = 'DISCLAIMER: Please verify below dates in graph slides below.'
	title2.text = 'Overview of projected collector-swap dates.'
	pic1_path = 'output//table_summary.png'
	pic2_path = 'output//table_legend.png'

	# Image 1 placement
	left1 = Cm(1)
	top1 = Cm(3.8)
	width1 = Cm(20)
	pic1 = slide.shapes.add_picture(pic1_path, left1, top1, width=width1)

	# Image 2 placement
	top2 = top1
	width2 = Cm(3)
	left2 = width1 + Cm(1)

	pic2 = slide.shapes.add_picture(pic2_path, left2, top2, width=width2)
	pic2.crop_bottom = 0.1
	pic2.crop_top = 0.1
	pic2.crop_left = 0.1
	pic2.crop_right = 0.1
	prs.save(filename)
